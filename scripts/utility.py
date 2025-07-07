# Script: `.\scripts\utility.py`

# Imports
import os
import subprocess
from tkinter import Tk, filedialog
from scripts.temporary import (
    FOLDER_LOCATION, FORMAT_FROM, FORMAT_TO, DELETE_FILES_AFTER,
    FILES_PROCESS_DONE, FILES_PROCESS_TOTAL, NCONVERT_PATH
)

def set_folder_location(new_location):
    """Update the global folder location."""
    global FOLDER_LOCATION
    if new_location and os.path.exists(new_location):
        FOLDER_LOCATION = new_location
    return FOLDER_LOCATION

def set_format_from(new_format):
    """Update the source format."""
    global FORMAT_FROM
    if new_format:
        FORMAT_FROM = new_format.upper()
    return FORMAT_FROM

def set_format_to(new_format):
    """Update the target format."""
    global FORMAT_TO
    if new_format:
        FORMAT_TO = new_format.upper()
    return FORMAT_TO

def set_delete_files_after(should_delete):
    """Update the delete files setting."""
    global DELETE_FILES_AFTER
    DELETE_FILES_AFTER = bool(should_delete)
    return DELETE_FILES_AFTER

def browse_folder():
    """Open a folder selection dialog using tkinter."""
    try:
        root = Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory(initialdir=FOLDER_LOCATION)
        root.destroy()
        if folder_selected:
            return folder_selected
        return FOLDER_LOCATION
    except Exception as e:
        print(f"Error opening folder dialog: {e}")
        return FOLDER_LOCATION

def find_files_to_convert():
    """Find all files matching the source format in the specified folder."""
    if not os.path.exists(FOLDER_LOCATION):
        try:
            # Try to create as current user if possible
            import pwd
            uid = pwd.getpwnam(os.getlogin()).pw_uid
            os.makedirs(FOLDER_LOCATION, exist_ok=True)
            os.chown(FOLDER_LOCATION, uid, -1)
        except Exception as e:
            print(f"Error creating directory: {e}")
            return []
    
    files = []
    try:
        for root, _, filenames in os.walk(FOLDER_LOCATION):
            for filename in filenames:
                if filename.lower().endswith(f".{FORMAT_FROM.lower()}"):
                    files.append(os.path.join(root, filename))
    except (PermissionError, OSError) as e:
        print(f"Error accessing directory: {e}")
    
    return files

def start_conversion():
    """Execute the conversion process using nconvert."""
    global FILES_PROCESS_DONE, FILES_PROCESS_TOTAL

    # Validate nconvert
    if not os.path.isfile(NCONVERT_PATH):
        return f"Error: nconvert not found at {NCONVERT_PATH}"
    
    if not os.access(NCONVERT_PATH, os.X_OK):
        return f"Error: nconvert at {NCONVERT_PATH} is not executable"

    if not os.path.exists(FOLDER_LOCATION):
        return "Error: Please set a valid folder location."
    
    files = find_files_to_convert()
    
    if not files:
        return f"No files with extension '{FORMAT_FROM}' found in {FOLDER_LOCATION}."
    
    FILES_PROCESS_DONE = 0
    FILES_PROCESS_TOTAL = len(files)
    conversion_results = []
    status_message = f"Starting conversion of {FILES_PROCESS_TOTAL} files...\n"

    for i, input_file in enumerate(files, 1):
        try:
            # Create output filename
            base_name = input_file.rsplit('.', 1)[0]
            output_file = f"{base_name}.{FORMAT_TO.lower()}"
            
            # Build nconvert command
            command = [
                NCONVERT_PATH,
                "-out", FORMAT_TO.lower(),
                "-overwrite",
                "-o", output_file,
                input_file
            ]
            
            # Execute conversion
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                FILES_PROCESS_DONE += 1
                conversion_results.append((input_file, True, ""))
                status_message += f"[{i}/{FILES_PROCESS_TOTAL}] Converted: {os.path.basename(input_file)}\n"
            else:
                error_message = result.stderr.strip() if result.stderr else "Unknown error occurred"
                conversion_results.append((input_file, False, error_message))
                status_message += f"[{i}/{FILES_PROCESS_TOTAL}] Failed: {os.path.basename(input_file)} - {error_message}\n"
                
        except subprocess.TimeoutExpired:
            conversion_results.append((input_file, False, "Conversion timeout"))
            status_message += f"[{i}/{FILES_PROCESS_TOTAL}] Timeout: {os.path.basename(input_file)}\n"
        except Exception as e:
            conversion_results.append((input_file, False, str(e)))
            status_message += f"[{i}/{FILES_PROCESS_TOTAL}] Error: {os.path.basename(input_file)} - {str(e)}\n"

    # Delete original files if requested
    if DELETE_FILES_AFTER:
        deleted_count = 0
        for input_file, success, _ in conversion_results:
            if success:
                try:
                    os.remove(input_file)
                    deleted_count += 1
                except Exception as e:
                    status_message += f"Failed to delete {os.path.basename(input_file)}: {str(e)}\n"
        
        if deleted_count > 0:
            status_message += f"Deleted {deleted_count} original files.\n"

    # Final summary
    failed_count = FILES_PROCESS_TOTAL - FILES_PROCESS_DONE
    status_message += f"\n=== CONVERSION SUMMARY ===\n"
    status_message += f"Total files processed: {FILES_PROCESS_TOTAL}\n"
    status_message += f"Successfully converted: {FILES_PROCESS_DONE}\n"
    status_message += f"Failed conversions: {failed_count}\n"

    return status_message
