# Script: `.\installer.py`

# Imports
import os
import sys
import subprocess
import urllib.request
import tarfile
import tempfile
import shutil
import platform
from typing import List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NCONVERT_DIR = os.path.join(DATA_DIR, 'NConvert-linux64')
NCONVERT_URL = "https://download.xnview.com/old_versions/NConvert/NConvert-7.221-linux64.tgz"

# System requirements
REQUIRED_SYSTEM_DEPS = {
    'tar': {'ubuntu': 'tar', 'test': ['tar', '--version']},
    'wget': {'ubuntu': 'wget', 'test': ['wget', '--version']},
    'tkinter': {'ubuntu': 'python3-tk', 'test': ['python3', '-c', '"import tkinter; print(tkinter.TkVersion)"']}
}

# Python package requirements
REQUIRED_PACKAGES = [
    'gradio',
    'pandas==2.1.3',
    'numpy==1.26.0',
    'psutil==6.1.1'
]

def check_system_dependencies() -> Tuple[bool, List[str]]:
    """Check for required system dependencies."""
    missing = []
    print("\nChecking system dependencies...")
    
    for dep, config in REQUIRED_SYSTEM_DEPS.items():
        try:
            # First try direct command test
            result = subprocess.run(
                config['test'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, config['test'])
                
            print(f"✓ {dep} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(config['ubuntu'])
            print(f"✗ {dep} not found")
    
    return (len(missing) == 0, missing)

def install_system_dependencies(packages: List[str]) -> bool:
    """Install missing system packages using apt."""
    if not packages:
        return True
        
    print(f"\nInstalling missing system packages: {', '.join(packages)}")
    try:
        result = subprocess.run(
            ['sudo', 'apt-get', 'install', '-y'] + packages,
            check=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Failed to install system packages: {e}")
        return False

def install_nconvert() -> bool:
    """Download and install NConvert binary."""
    print("\nInstalling NConvert...")
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            print(f"Downloading to {temp_path}...")
            urllib.request.urlretrieve(NCONVERT_URL, temp_path)

        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Extracting to {temp_dir}...")
            with tarfile.open(temp_path, 'r:gz') as tar:
                tar.extractall(temp_dir)

            extracted_items = os.listdir(temp_dir)
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_dir, extracted_items[0])):
                source_dir = os.path.join(temp_dir, extracted_items[0])
                if os.path.exists(NCONVERT_DIR):
                    shutil.rmtree(NCONVERT_DIR)
                shutil.move(source_dir, NCONVERT_DIR)
                
                # Make nconvert executable
                nconvert_path = os.path.join(NCONVERT_DIR, 'nconvert')
                if os.path.isfile(nconvert_path):
                    os.chmod(nconvert_path, 0o755)
                    print("✓ NConvert installed and made executable")
                    return True
            else:
                print("✗ Unexpected archive structure")
                
        os.remove(temp_path)
    except Exception as e:
        print(f"✗ NConvert installation failed: {e}")
    
    return False

def install_python_packages() -> bool:
    """Install required Python packages."""
    print("\nInstalling Python packages...")
    try:
        requirements_path = os.path.join(DATA_DIR, 'requirements.txt')
        with open(requirements_path, 'w') as f:
            for package in REQUIRED_PACKAGES:
                f.write(f"{package}\n")

        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', requirements_path],
            check=True,
            text=True
        )
        print("✓ Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python packages: {e.stderr}")
        return False

def main():
    print("NConvert-Bash Installer")
    print("=======================")
    
    # Verify Linux system
    if platform.system() != 'Linux':
        print("Error: This installer is only for Linux systems")
        sys.exit(1)

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Check and install system dependencies
    deps_ok, missing_deps = check_system_dependencies()
    if not deps_ok:
        if not install_system_dependencies(missing_deps):
            print("\nError: Could not install all system dependencies")
            print("Please run manually: sudo apt-get install", " ".join(missing_deps))
            sys.exit(1)
            
    # Install NConvert
    if not install_nconvert():
        sys.exit(1)
        
    # Install Python packages
    if not install_python_packages():
        sys.exit(1)

    print("\nInstallation completed successfully!")
    print("You can now run the program using: ./NConvert-Bash.sh")

if __name__ == "__main__":
    main()