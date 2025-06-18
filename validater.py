# Script: `.\validation.py`

# Imports
import os
import sys
import subprocess
import importlib
import pkg_resources

# Directory and package constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NCONVERT_DIR = os.path.join(DATA_DIR, 'NConvert-linux64')
NCONVERT_PATH = os.path.join(NCONVERT_DIR, 'nconvert')
VENV_DIR = os.path.join(BASE_DIR, 'venv')  # Added venv reference

REQUIRED_PACKAGES = [
    'gradio',
    'pandas==2.1.3',
    'numpy==1.26.0',
    'psutil==6.1.1'
]
PACKAGE_IMPORT_MAP = {
    'gradio': 'gradio',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'psutil': 'psutil'
}

def print_status(message, success=True):
    """Print a status message with a checkmark or cross."""
    symbol = "✓" if success else "✗"
    print(f"{symbol} {message}")

def check_venv():
    """Check if virtual environment exists."""
    if not os.path.exists(VENV_DIR):
        print_status("Virtual environment not found", success=False)
        return False
    print_status("Virtual environment exists")
    return True

def check_nconvert():
    """Validate the presence and executability of the nconvert binary."""
    if not os.path.isfile(NCONVERT_PATH):
        print_status(f"nconvert not found at {NCONVERT_PATH}", success=False)
        return False

    if not os.access(NCONVERT_PATH, os.X_OK):
        print_status(f"nconvert at {NCONVERT_PATH} is not executable", success=False)
        return False

    try:
        result = subprocess.run(
            [NCONVERT_PATH, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print_status(f"nconvert found: {version}")
            return True
        else:
            print_status(f"nconvert failed to run: {result.stderr.strip()}", success=False)
            return False
    except subprocess.TimeoutExpired:
        print_status("nconvert execution timed out", success=False)
        return False
    except Exception as e:
        print_status(f"Error testing nconvert: {e}", success=False)
        return False

def check_python_packages():
    """Verify that all required Python packages are installed and importable."""
    all_good = True
    for package in REQUIRED_PACKAGES:
        package_name = package.split('==')[0]
        import_name = PACKAGE_IMPORT_MAP.get(package_name, package_name.replace('-', '_'))
        try:
            installed_version = pkg_resources.get_distribution(package_name).version
            expected_version = package.split('==')[1] if '==' in package else None
            if expected_version and installed_version != expected_version:
                print_status(
                    f"{package_name} version mismatch: expected {expected_version}, found {installed_version}",
                    success=False
                )
                all_good = False
                continue

            importlib.import_module(import_name)
            print_status(f"{package_name} (version {installed_version}) is importable")
        except pkg_resources.DistributionNotFound:
            print_status(f"{package_name} is not installed", success=False)
            all_good = False
        except ImportError as e:
            print_status(f"Failed to import {package_name}: {e}", success=False)
            all_good = False
        except Exception as e:
            print_status(f"Error checking {package_name}: {e}", success=False)
            all_good = False
    return all_good

def main():
    """Main function to validate all components."""
    print("NConvert-Bash Validation")
    print("=======================")

    all_good = True

    # Validate virtual environment
    print("\nChecking virtual environment...")
    if not check_venv():
        all_good = False

    # Validate nconvert
    print("\nChecking NConvert...")
    if not check_nconvert():
        all_good = False

    # Validate Python packages
    print("\nChecking Python packages...")
    if not check_python_packages():
        all_good = False

    # Final summary
    print("\nValidation Summary")
    print("------------------")
    if all_good:
        print_status("All components validated successfully")
    else:
        print_status("Some components failed validation", success=False)
        print("\nPlease run the installer (option 2) to fix missing or incorrect components.")

    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()