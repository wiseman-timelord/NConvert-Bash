# Script: `.\installer.py`

# Imports
import os
import sys
import subprocess
import urllib.request
import tarfile
import tempfile
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NCONVERT_DIR = os.path.join(DATA_DIR, 'NConvert-linux64')
NCONVERT_URL = "https://download.xnview.com/old_versions/NConvert/NConvert-7.221-linux64.tgz"
REQUIRED_PACKAGES = [
    'gradio',
    'pandas==2.1.3',
    'numpy==1.26.0',
    'psutil==6.1.1'
]

def main():
    print("NConvert-Bash Installer")
    print("=======================")

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Download and install NConvert
    print("Installing NConvert...")
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
            else:
                print("Unexpected archive structure.")
                sys.exit(1)

        os.remove(temp_path)
        print("NConvert installed successfully.")
    except urllib.error.URLError as e:
        print(f"Download failed: {e}")
        sys.exit(1)
    except tarfile.TarError as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Install Python packages
    print("\nInstalling Python packages...")
    requirements_path = os.path.join(DATA_DIR, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        for package in REQUIRED_PACKAGES:
            f.write(f"{package}\n")

    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', requirements_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Failed to install packages:")
        print(result.stderr)
        sys.exit(1)
    else:
        print("Packages installed successfully.")

    print("\nInstallation complete.")

if __name__ == "__main__":
    main()
