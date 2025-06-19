# Validate NConvert-Bash installation
import os
import sys
import subprocess

# Get config from installer
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from installer import REQUIRED_PACKAGES, BASE_DIR, DATA_DIR, NCONVERT_DIR, VENV_DIR, TEMP_DIR
    print("✓ Config imported")
except ImportError as e:
    print(f"✗ Config import failed: {e}")
    sys.exit(1)

def print_status(msg, ok=True):
    print(f"{'✓' if ok else '✗'} {msg}")

def check_venv():
    if not os.path.exists(VENV_DIR):
        print_status("Venv missing", False)
        return False
    
    required = [
        os.path.join(VENV_DIR, 'bin', 'python'),
        os.path.join(VENV_DIR, 'bin', 'pip')
    ]
    
    for item in required:
        if not os.path.exists(item):
            print_status(f"Missing: {os.path.basename(item)}", False)
            return False
    
    print_status("Venv valid")
    return True

def check_nconvert():
    nconvert_path = None
    if os.path.exists(NCONVERT_DIR):
        for root, _, files in os.walk(NCONVERT_DIR):
            if 'nconvert' in files:
                nconvert_path = os.path.join(root, 'nconvert')
                break
    
    if not nconvert_path:
        print_status("NConvert binary missing", False)
        return False

    if not os.access(nconvert_path, os.X_OK):
        print_status("NConvert not executable", False)
        return False
    
    print_status("NConvert present and executable")
    return True

def check_packages():
    if not check_venv():
        print_status("Skipped packages", False)
        return False
    
    venv_python = os.path.join(VENV_DIR, 'bin', 'python')
    all_ok = True

    # First check if all packages are installed
    missing_packages = []
    for pkg in REQUIRED_PACKAGES:
        name = pkg.split('==')[0]
        if name == 'PyGObject':  # Skip PyGObject (handled by symlink)
            continue
            
        cmd = f'import importlib.util; print(importlib.util.find_spec("{name}") is not None)'
        try:
            result = subprocess.run(
                [venv_python, '-c', cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0 or 'True' not in result.stdout:
                missing_packages.append(name)
        except Exception:
            missing_packages.append(name)
    
    if not missing_packages:
        print_status("Libraries installed")
        print_status("Dependencies installed")
        return True
    else:
        for pkg in missing_packages:
            print_status(f"{pkg} missing", False)
        return False

def check_dirs():
    required_dirs = [
        DATA_DIR,
        NCONVERT_DIR,
        VENV_DIR,
        TEMP_DIR
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_status(f"Dir exists: {os.path.basename(dir_path)}")
        else:
            print_status(f"Missing dir: {os.path.basename(dir_path)}", False)
            all_ok = False
    
    return all_ok

def check_symlinks():
    # Verify PyGObject symlink exists
    venv_site_packages = os.path.join(VENV_DIR, 'lib', 
        f'python{sys.version_info.major}.{sys.version_info.minor}', 
        'site-packages')
    
    gi_symlink = os.path.join(venv_site_packages, 'gi')
    gi_system_path = '/usr/lib/python3/dist-packages/gi'
    
    if os.path.islink(gi_symlink) and os.readlink(gi_symlink) == gi_system_path:
        print_status("PyGObject symlink valid")
        return True
    else:
        print_status("PyGObject symlink missing", False)
        return False

def main():
    os.system('clear')
    print("="*80)
    print("    NConvert-Bash - Validation")
    print("="*80)
    print()

    checks = [
        ("Directories", check_dirs),
        ("Virtual Env", check_venv),
        ("NConvert", check_nconvert),
        ("PyGObject Symlink", check_symlinks),
        ("Packages", check_packages)
    ]

    all_ok = True
    for name, func in checks:
        print(f"Checking {name}...")
        if not func():
            all_ok = False

    if all_ok:
        print_status("All checks passed")
    else:
        print_status("Validation failed", False)
        print("Run the installer to fix issues")
    print()
    
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()