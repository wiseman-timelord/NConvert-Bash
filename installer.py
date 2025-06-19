# Script: `.\installer.py`

# Imports
import os
import sys
import subprocess
import urllib.request
import tarfile
import shutil
import platform
import time
from typing import List, Tuple, Dict

# Directory structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')
NCONVERT_DIR = os.path.join(DATA_DIR, 'NConvert-linux64')
VENV_DIR = os.path.join(BASE_DIR, 'venv')

# URLs and downloads
NCONVERT_URL = "https://download.xnview.com/NConvert-linux64.tgz"
NCONVERT_ARCHIVE = os.path.join(TEMP_DIR, 'NConvert-linux64.tgz')

# System requirements with Ubuntu 24.10 compatibility
REQUIRED_SYSTEM_DEPS = {
    # Core utilities
    'tar': {
        'packages': ['tar'], 
        'test': ['tar', '--version']
    },
    'wget': {
        'packages': ['wget'], 
        'test': ['wget', '--version']
    },
    'curl': {
        'packages': ['curl'], 
        'test': ['curl', '--version']
    },
    
    # Python environment
    'python3-venv': {
        'packages': ['python3-venv'], 
        'test': ['python3', '-m', 'venv', '--help']
    },
    'python3-pip': {
        'packages': ['python3-pip'], 
        'test': ['python3', '-m', 'pip', '--version']
    },
    'python3-tk': {
        'packages': ['python3-tk'], 
        'test': ['python3', '-c', 'import tkinter; print("Tkinter available")']
    },
    'python3-dev': {
        'packages': ['python3-dev'], 
        'test': ['dpkg', '-s', 'python3-dev']
    },
    
    # GTK3 stack - Ubuntu 24.10 compatibility
    'libgtk-3-0': {
        'packages': ['libgtk-3-0t64'],  # Ubuntu 24.04+ uses t64 suffix
        'test': ['dpkg', '-l', 'libgtk-3-0t64']
    },
    'libgtk-3-dev': {
        'packages': ['libgtk-3-dev'], 
        'test': ['dpkg', '-s', 'libgtk-3-dev']
    },
    'gir1.2-gtk-3.0': {
        'packages': ['gir1.2-gtk-3.0'], 
        'test': ['dpkg', '-s', 'gir1.2-gtk-3.0']
    },
    
    # GObject Introspection - Ubuntu 24.10 compatibility
    'gobject-introspection': {
        'packages': ['gobject-introspection'], 
        'test': ['dpkg', '-s', 'gobject-introspection']
    },
    'libgirepository-dev': {
        'packages': ['libgirepository1.0-dev'],  # Correct package for Ubuntu 24.10
        'test': ['dpkg', '-s', 'libgirepository1.0-dev']
    },
    'python3-gi': {
        'packages': ['python3-gi'], 
        'test': ['dpkg', '-s', 'python3-gi']
    },
    
    # Graphics dependencies
    'libcairo2-dev': {
        'packages': ['libcairo2-dev'], 
        'test': ['dpkg', '-s', 'libcairo2-dev']
    },
    'libgdk-pixbuf2.0-dev': {
        'packages': ['libgdk-pixbuf-2.0-dev'],  # Correct package name
        'test': ['dpkg', '-s', 'libgdk-pixbuf-2.0-dev']
    },
    
    # Build tools
    'build-essential': {
        'packages': ['build-essential'], 
        'test': ['dpkg', '-s', 'build-essential']
    },
    'pkg-config': {
        'packages': ['pkg-config'], 
        'test': ['pkg-config', '--version']
    },
    'meson': {
        'packages': ['meson'], 
        'test': ['meson', '--version']
    },
    'ninja-build': {
        'packages': ['ninja-build'], 
        'test': ['ninja', '--version']
    },
    
    # Python build dependencies - Ubuntu 24.10 compatibility
    'python3-setuptools': {
        'packages': ['python3-setuptools'],  # Replaces python3-distutils
        'test': ['python3', '-c', 'import setuptools; print("setuptools available")']
    }
}

# Python package requirements
REQUIRED_PACKAGES = [
    'gradio',
    'pandas==2.1.3',
    'numpy==1.26.0',
    'psutil==6.1.1',
    'tk',
    'PyGObject' 
]

def get_ubuntu_version() -> Tuple[str, str]:
    """Get Ubuntu version information."""
    try:
        result = subprocess.run(['lsb_release', '-rs'], capture_output=True, text=True)
        version = result.stdout.strip()
        
        result = subprocess.run(['lsb_release', '-cs'], capture_output=True, text=True)  
        codename = result.stdout.strip()
        
        return version, codename
    except:
        return "unknown", "unknown"

def cleanup_existing_installation():
    """Clean up any existing installation for fresh install."""
    print("\nCleaning up existing installation...")
    
    # Remove virtual environment
    if os.path.exists(VENV_DIR):
        try:
            shutil.rmtree(VENV_DIR)
            print("✓ Removed existing virtual environment")
        except Exception as e:
            print(f"✗ Failed to remove existing venv: {e}")
            return False
    
    # Remove data directory (including NConvert and temp)
    if os.path.exists(DATA_DIR):
        try:
            shutil.rmtree(DATA_DIR)
            print("✓ Removed existing data directory")
        except Exception as e:
            print(f"✗ Failed to remove existing data directory: {e}")
            return False
    
    return True

def create_directory_structure():
    """Create all necessary directories for the project."""
    print("\nCreating directory structure...")
    directories = [
        DATA_DIR,
        TEMP_DIR,
        # VENV_DIR will be created by venv module
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created/verified directory: {directory}")
        except Exception as e:
            print(f"✗ Failed to create directory {directory}: {e}")
            return False
    
    return True

def cleanup_temp_files():
    """Clean up temporary files after installation."""
    print("\nCleaning up temporary files...")
    try:
        if os.path.exists(NCONVERT_ARCHIVE):
            os.remove(NCONVERT_ARCHIVE)
            print("✓ Removed temporary download file")
        
        # Clean any other temp files
        if os.path.exists(TEMP_DIR):
            for file in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"✓ Removed temporary file: {file}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"✓ Removed temporary directory: {file}")
        
        return True
    except Exception as e:
        print(f"✗ Error cleaning temp files: {e}")
        return False

def check_system_dependencies() -> Tuple[bool, List[str]]:
    """Check for required system dependencies with smart package resolution."""
    missing = []
    available_packages = []
    
    print("\nChecking system dependencies...")
    ubuntu_version, ubuntu_codename = get_ubuntu_version()
    print(f"Detected Ubuntu {ubuntu_version} ({ubuntu_codename})")
    
    for dep_name, config in REQUIRED_SYSTEM_DEPS.items():
        try:
            # Special handling for different test types
            if dep_name == 'python3-tk':
                result = subprocess.run(
                    config['test'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, config['test'])
            elif dep_name == 'python3-setuptools':
                # Special test for setuptools
                result = subprocess.run(
                    config['test'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, config['test'])
            elif 'dpkg' in config['test'][0]:
                # Handle dpkg checks
                if ' -l ' in ' '.join(config['test']):
                    # Package listing check
                    result = subprocess.run(
                        config['test'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=10
                    )
                    # Check if package is installed
                    if result.returncode != 0 or "no packages found" in result.stdout:
                        raise Exception(f"Package not installed: {dep_name}")
                else:
                    # Standard dpkg status check
                    result = subprocess.run(
                        config['test'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=10
                    )
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, config['test'])
            else:
                # Generic command check
                result = subprocess.run(
                    config['test'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, config['test'])
                    
            print(f"✓ {dep_name} is available")
            
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
            # Add all packages in the config to missing list
            missing.extend(config['packages'])
            print(f"✗ {dep_name} not found (will install: {', '.join(config['packages'])})")
    
    return (len(missing) == 0, list(set(missing)))  # Remove duplicates

def install_system_dependencies(packages: List[str]) -> bool:
    """Install missing system packages using apt with better error handling."""
    if not packages:
        return True
        
    print(f"\nInstalling missing system packages: {', '.join(packages)}")
    
    try:
        # Update package list
        print("Updating package list...")
        result = subprocess.run(
            ['sudo', 'apt-get', 'update'],
            check=True,
            text=True,
            timeout=300
        )
        
        # Install packages in a single command for efficiency
        print("Installing packages...")
        result = subprocess.run(
            ['sudo', 'apt-get', 'install', '-y'] + packages,
            check=True,
            text=True,
            timeout=600
        )
        
        print("✓ System packages installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Package installation failed: {e}")
        print("Attempting to install packages individually...")
        
        # Try installing packages one by one
        success = True
        for package in packages:
            try:
                print(f"Installing {package} individually...")
                subprocess.run(
                    ['sudo', 'apt-get', 'install', '-y', package],
                    check=True,
                    text=True,
                    timeout=300
                )
                print(f"✓ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")
                success = False
                
        return success
        
    except subprocess.TimeoutExpired:
        print("✗ Package installation timed out")
        return False

class DownloadProgressBar:
    """Compact progress bar for file downloads - fits in 80 char width."""
    
    def __init__(self, total_size: int, existing_size: int = 0):
        self.total_size = total_size
        self.downloaded = existing_size
        self.start_time = time.time()
        self.last_update = 0
        
    def update(self, chunk_size: int):
        """Update progress bar with new chunk."""
        self.downloaded += chunk_size
        current_time = time.time()
        
        # Update every 0.5 seconds to avoid too frequent updates
        if current_time - self.last_update < 0.5 and self.downloaded < self.total_size:
            return
            
        self.last_update = current_time
        self.display()
        
    def display(self):
        """Display the current progress."""
        elapsed_time = time.time() - self.start_time
        
        # Calculate progress percentage
        if self.total_size > 0:
            progress = (self.downloaded / self.total_size) * 100
        else:
            progress = 0
        
        # Create progress bar (10 characters)
        bar_length = 10
        filled_length = int(bar_length * self.downloaded // self.total_size) if self.total_size > 0 else 0
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Format sizes
        def format_size(size):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f}{unit}"
                size /= 1024.0
            return f"{size:.1f}TB"
        
        # Calculate speed
        if elapsed_time > 0:
            speed = self.downloaded / elapsed_time
        else:
            speed = 0
        
        # Format time
        def format_time(seconds):
            if seconds < 60:
                return f"{seconds:.0f}s"
            elif seconds < 3600:
                return f"{seconds//60:.0f}m{seconds%60:.0f}s"
            else:
                return f"{seconds//3600:.0f}h{(seconds%3600)//60:.0f}m"
        
        # Calculate ETA
        if speed > 0 and self.downloaded < self.total_size:
            remaining_time = (self.total_size - self.downloaded) / speed
            eta_str = format_time(remaining_time)
        else:
            eta_str = "0s"
        
        # Compact format: [██████░░░░] 64.2%, 9.8MB/15.3MB, 1.0MB/s, 12s/18s
        if self.downloaded < self.total_size:
            progress_line = (
                f"\r[{bar}] {progress:4.1f}%, "
                f"{format_size(self.downloaded)}/{format_size(self.total_size)}, "
                f"{format_size(speed)}/s, "
                f"{format_time(elapsed_time)}/{eta_str}"
            )
        else:
            progress_line = (
                f"\r[{bar}] 100.0%, "
                f"{format_size(self.downloaded)}/{format_size(self.total_size)}, "
                f"Done in {format_time(elapsed_time)}"
            )
        
        # Ensure we fit in 80 characters and clear any leftover text
        if len(progress_line) > 79:
            progress_line = progress_line[:76] + "..."
        progress_line = progress_line.ljust(79)
        
        print(progress_line, end='', flush=True)
        
        # Print newline when complete
        if self.downloaded >= self.total_size:
            print()

def download_with_resume(url: str, filepath: str, max_retries: int = 3) -> bool:
    """Download a file with resume capability and retry logic."""
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"\nRetry attempt {attempt + 1}/{max_retries}...")
            
            # Check if file already exists (for resume)
            existing_size = 0
            if os.path.exists(filepath):
                existing_size = os.path.getsize(filepath)
                print(f"Found existing file: {existing_size:,} bytes")
            
            # Create request with resume header if file exists
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            
            if existing_size > 0:
                req.add_header('Range', f'bytes={existing_size}-')
            
            # Open connection
            with urllib.request.urlopen(req, timeout=60) as response:
                # Handle partial content (206) or full content (200)
                if response.code == 206:
                    # Partial content - resuming
                    content_range = response.headers.get('Content-Range', '')
                    if content_range:
                        # Parse "bytes start-end/total"
                        total_size = int(content_range.split('/')[-1])
                    else:
                        total_size = existing_size + int(response.headers.get('Content-Length', 0))
                    print(f"Resuming download from byte {existing_size:,}")
                elif response.code == 200:
                    # Full content
                    if existing_size > 0:
                        print("Server doesn't support resume, restarting download")
                        os.remove(filepath)
                        existing_size = 0
                    total_size = int(response.headers.get('Content-Length', 0))
                else:
                    raise Exception(f"Unexpected HTTP status: {response.code}")
                
                print(f"Total file size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
                
                # Initialize progress bar
                progress_bar = DownloadProgressBar(total_size, existing_size)
                
                # Open file in append mode if resuming, write mode if starting fresh
                file_mode = 'ab' if existing_size > 0 else 'wb'
                with open(filepath, file_mode) as f:
                    chunk_size = 32768  # 32KB chunks
                    
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        progress_bar.update(len(chunk))
                
                # Verify download completeness
                actual_size = os.path.getsize(filepath)
                if total_size > 0 and actual_size != total_size:
                    raise Exception(f"Download incomplete: got {actual_size:,} bytes, expected {total_size:,}")
                
                print("✓ Download completed successfully")
                return True
                
        except urllib.error.HTTPError as e:
            if e.code == 416:  # Range Not Satisfiable - file might be complete
                actual_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
                # Try to get the real file size
                try:
                    head_req = urllib.request.Request(url)
                    head_req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64)')
                    head_req.get_method = lambda: 'HEAD'
                    with urllib.request.urlopen(head_req, timeout=30) as head_response:
                        expected_size = int(head_response.headers.get('Content-Length', 0))
                        if actual_size == expected_size:
                            print("✓ File already completely downloaded")
                            return True
                except:
                    pass
            print(f"✗ Download attempt {attempt + 1} failed: HTTP {e.code} - {e.reason}")
        except Exception as e:
            print(f"✗ Download attempt {attempt + 1} failed: {e}")
            
        if attempt < max_retries - 1:
            print("Waiting 2 seconds before retry...")
            time.sleep(2)
        else:
            print("All download attempts failed")
            # Clean up corrupted file on final failure
            if os.path.exists(filepath):
                os.remove(filepath)
            return False
    
    return False

def install_nconvert() -> bool:
    """Download and install NConvert binary."""
    print("\nInstalling NConvert...")
    try:
        # Download to our temp directory
        print(f"Downloading NConvert from {NCONVERT_URL}...")
        print(f"Saving to {NCONVERT_ARCHIVE}...")
        print()  # Empty line before progress bar
        
        # Download with resume capability
        if not download_with_resume(NCONVERT_URL, NCONVERT_ARCHIVE):
            raise Exception("Failed to download NConvert after multiple attempts")

        # Verify download exists and has content
        if not os.path.exists(NCONVERT_ARCHIVE) or os.path.getsize(NCONVERT_ARCHIVE) == 0:
            raise Exception("Downloaded file is empty or missing")

        # Extract to temp directory first
        print(f"Extracting archive...")
        extract_temp_dir = os.path.join(TEMP_DIR, 'extract')
        os.makedirs(extract_temp_dir, exist_ok=True)
        
        # More robust extraction with better error handling
        try:
            with tarfile.open(NCONVERT_ARCHIVE, 'r:gz') as tar:
                # Security check: ensure no path traversal
                for member in tar.getmembers():
                    if os.path.isabs(member.name) or ".." in member.name:
                        raise Exception(f"Unsafe path in archive: {member.name}")
                
                # Extract all members
                tar.extractall(extract_temp_dir)
                print("✓ Archive extracted successfully")
                
        except tarfile.ReadError as e:
            raise Exception(f"Archive appears to be corrupted or incomplete: {e}")
        except Exception as e:
            raise Exception(f"Failed to extract archive: {e}")

        # Find the extracted directory or files
        extracted_items = os.listdir(extract_temp_dir)
        if not extracted_items:
            raise Exception("No files extracted from archive")
            
        # Remove existing NConvert directory if it exists
        if os.path.exists(NCONVERT_DIR):
            shutil.rmtree(NCONVERT_DIR)
            print("✓ Removed existing NConvert installation")
        
        # Handle different archive structures
        if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_temp_dir, extracted_items[0])):
            # Archive contains a directory
            source_dir = os.path.join(extract_temp_dir, extracted_items[0])
            shutil.move(source_dir, NCONVERT_DIR)
        else:
            # Archive contains files directly
            os.makedirs(NCONVERT_DIR, exist_ok=True)
            for item in extracted_items:
                source_path = os.path.join(extract_temp_dir, item)
                dest_path = os.path.join(NCONVERT_DIR, item)
                if os.path.isdir(source_path):
                    shutil.move(source_path, dest_path)
                else:
                    shutil.move(source_path, dest_path)
        
        # Find and make nconvert executable
        nconvert_path = None
        for root, dirs, files in os.walk(NCONVERT_DIR):
            if 'nconvert' in files:
                nconvert_path = os.path.join(root, 'nconvert')
                break
        
        if nconvert_path and os.path.isfile(nconvert_path):
            os.chmod(nconvert_path, 0o755)
            print("✓ NConvert installed and made executable")
            
            # Clean up extraction temp directory
            if os.path.exists(extract_temp_dir):
                shutil.rmtree(extract_temp_dir)
            return True
        else:
            print("✗ nconvert binary not found in extracted files")
            return False
            
    except Exception as e:
        print(f"✗ NConvert installation failed: {e}")
        # Clean up on failure
        if os.path.exists(NCONVERT_DIR):
            shutil.rmtree(NCONVERT_DIR)
        if os.path.exists(NCONVERT_ARCHIVE):
            os.remove(NCONVERT_ARCHIVE)
        return False

def create_virtual_environment() -> bool:
    """Create a Python virtual environment."""
    print("\nCreating Python virtual environment...")
    try:
        # Create new venv
        result = subprocess.run(
            [sys.executable, '-m', 'venv', VENV_DIR],
            check=True,
            text=True,
            timeout=120
        )
        print(f"✓ Virtual environment created at {VENV_DIR}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Virtual environment creation timed out")
        return False

def install_python_packages() -> bool:
    """Install required Python packages in virtual environment."""
    print("\nInstalling Python packages in virtual environment...")
    try:
        pip_executable = os.path.join(VENV_DIR, 'bin', 'pip')
        
        # Upgrade pip first
        print("Upgrading pip...")
        subprocess.run(
            [pip_executable, 'install', '--upgrade', 'pip'],
            check=True,
            text=True,
            timeout=120
        )
        
        # Create symlink for system PyGObject if it exists
        gi_path = '/usr/lib/python3/dist-packages/gi'
        venv_site_packages = os.path.join(VENV_DIR, 'lib', 
            f'python{sys.version_info.major}.{sys.version_info.minor}', 
            'site-packages')
        gi_symlink = os.path.join(venv_site_packages, 'gi')
        
        if os.path.exists(gi_path) and not os.path.exists(gi_symlink):
            try:
                os.symlink(gi_path, gi_symlink)
                print("✓ System PyGObject linked to virtual environment")
            except Exception as e:
                print(f"⚠️ Could not link PyGObject: {e}")

        # Install remaining packages with retry logic
        for package in REQUIRED_PACKAGES:
            if package == 'PyGObject':
                # Skip PyGObject as we're using the system version
                print("Skipping PyGObject installation (using system package)")
                continue
                
            print(f"Installing {package}...")
            for attempt in range(3):
                try:
                    subprocess.run(
                        [pip_executable, 'install', package],
                        check=True,
                        text=True,
                        timeout=300
                    )
                    print(f"✓ Installed {package}")
                    break
                except subprocess.CalledProcessError as e:
                    if attempt == 2:
                        print(f"✗ Failed to install {package} after 3 attempts")
                        return False
                    print(f"⚠️ Retry {attempt+1}/3 for {package}...")
                    time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"✗ Package installation failed: {e}")
        return False

def main():
    os.system('clear')
    print("="*80)
    print("NConvert-Bash - Installation")
    print("="*80)
    print("")
    
    # Verify Linux system
    if platform.system() != 'Linux':
        print("Error: This installer is only for Linux systems")
        sys.exit(1)

    # Clean up existing installation first
    if not cleanup_existing_installation():
        print("\nError: Could not clean up existing installation")
        sys.exit(1)

    # Create directory structure
    if not create_directory_structure():
        print("\nError: Could not create directory structure")
        sys.exit(1)

    # Check and install system dependencies
    deps_ok, missing_deps = check_system_dependencies()
    if not deps_ok:
        print(f"\nMissing system dependencies: {', '.join(missing_deps)}")
        print("Attempting to install them...")
        if not install_system_dependencies(missing_deps):
            print("\nError: Could not install all system dependencies")
            print("Please run manually: sudo apt-get install", " ".join(missing_deps))
            sys.exit(1)
            
    # Install NConvert
    if not install_nconvert():
        print("\nError: NConvert installation failed")
        sys.exit(1)
        
    # Create virtual environment
    if not create_virtual_environment():
        print("\nError: Virtual environment creation failed")
        sys.exit(1)
        
    # Install Python packages
    if not install_python_packages():
        print("\nError: Python package installation failed")
        sys.exit(1)

    # Clean up temporary files
    cleanup_temp_files()

    print("\n" + "="*50)
    print("\nInstallation processes completed successfully!")
    print("\nRun the validation script to verify the installation.\n")

if __name__ == "__main__":
    main()