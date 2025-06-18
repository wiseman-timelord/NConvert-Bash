# Validate NConvert-Bash installation
import os
import sys
import subprocess

# Get config from installer
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from installer import REQUIRED_PACKAGES, BASE_DIR, DATA_DIR, NCONVERT_DIR, VENV_DIR
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
        print_status("NConvert missing", False)
        return False

    if not os.access(nconvert_path, os.X_OK):
        print_status("NConvert not executable", False)
        return False
    
    print_status("NConvert valid")
    return True

def check_packages():
    if not check_venv():
        print_status("Skipped packages", False)
        return False
    
    venv_python = os.path.join(VENV_DIR, 'bin', 'python')
    all_ok = True

    for pkg in REQUIRED_PACKAGES:
        name = pkg.split('==')[0]
        cmd = f'import importlib.metadata; print(importlib.metadata.version("{name}"))'
        
        try:
            result = subprocess.run(
                [venv_python, '-c', cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                raise Exception("Version check failed")
                
            print_status(f"{name} installed")
        except Exception:
            print_status(f"{name} missing", False)
            all_ok = False
    
    return all_ok

def check_dirs():
    required = [DATA_DIR, NCONVERT_DIR, VENV_DIR]
    all_ok = True
    
    for dir_path in required:
        if os.path.exists(dir_path):
            print_status(f"Dir exists: {os.path.basename(dir_path)}")
        else:
            print_status(f"Missing dir: {os.path.basename(dir_path)}", False)
            all_ok = False
    
    return all_ok

def main():
    os.system('clear')
    print("="*80)
    print("    NConvert-Bash - Validation")
    print("="*80)
    print("")

    checks = [
        ("Directories", check_dirs),
        ("Virtual Env", check_venv),
        ("NConvert", check_nconvert),
        ("Packages", check_packages)
    ]

    all_ok = True
    for name, func in checks:
        print(f"Checking {name}...")
        if not func():
            all_ok = False

    print("")
    if all_ok:
        print_status("All checks passed")
    else:
        print_status("Validation failed", False)
        print("Run installer option 2")
    print("")
    
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()