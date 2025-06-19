# NConvert-Bash
Status: Alpha (working on: primary testing)


### Description:
Its a Python Gradio interface for converting ~500 common/rare image formats to ~500 common/rare image formats, all made possible through `NConvert` linux native command line tool. The frontend/installer provides a user-friendly menu to set the source folder, input file format, and desired output format. The scripts ensures efficient and seamless conversion and management of image files, making it a practical tool for users needing to process many images in multiple common/rare formats

### Preview:
- Bash menu is looking good...
```
================================================================================
    NConvert-Bash
================================================================================






    1. Launch Main Program 

    2. Install Files/Libraries 

    3. Validate Files/Libraries 






--------------------------------------------------------------------------------
Selection; Menu Options 1-3, Exit Bash = X: 

```
- Validation of Files/Libraries...
```
================================================================================
    NConvert-Bash - Validation
================================================================================

Checking Directories...
✓ Dir exists: data
✓ Dir exists: NConvert-linux64
✓ Dir exists: venv
Checking Virtual Env...
✓ Venv valid
Checking NConvert...
✓ NConvert valid
Checking Packages...
✓ Venv valid
✓ gradio installed
✓ pandas installed
✓ numpy installed
✓ psutil installed

✓ All checks passed

--------------------------------------------------------------------------------
Press Enter to continue...

```

## Requirements:
- Linux - It will be tested on Ubuntu 24.10.
- [NConvert](https://www.xnview.com/en/nconvert) - ~500 image formats supported (installed by installer).
- Python 3.8+ - Compatible with what are now the lower versions of python.
- Python Libraries - The `.\Installer.py` puts all required libraries to the `.\.venv`, you can inspect them there if you like.
- System Dependencies - Things such as, `tkinter` and `libgtk`. Check "REQUIRED_SYSTEM_DEPS" in `.\Installer.py` for the full list.

### File Structure:
- Files in package...
```
.\NConvert-Bash.sh (bash script, "1. Run Main Program", "2. Install Files/Libraries", "3. Files/Libraries Validation".  
.\installer.py (standalone installer script)
.\validation.py (checks libraries and files are present/correct (standalone))
.\launcher.py (entry point for main program. Should contain "main" function.) 
.\scripts\temporary.py (Should contain all, global variables/constants, global maps/lists/etc.)
.\scripts\interface.py (Should contain, all concise printed terminal text, all gradio code)
.\scripts\utility.py (code not directly relevant to subling scripts and misc code)
```
- Files Created...
```
.\data\
.\data\temp\           # Temporary files (cleaned after install)
.\temp\NConvert-linux64\  # Installed NConvert binary/files
.\venv\               # Python virtual environment 
```

### Development
The current plan is...
1. Testing/bugfixing/improving, until working.
