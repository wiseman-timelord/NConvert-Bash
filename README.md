# NConvert-Bash
Status: Working.


### Description:
Its a Python Gradio interface for converting ~500 common/rare image formats to ~500 common/rare image formats, all made possible through `NConvert` linux native command line tool. The frontend/installer provides a user-friendly menu to set the source folder, input file format, and desired output format. The scripts ensures efficient and seamless conversion and management of image files, making it a practical tool for users needing to process many images in multiple common/rare formats. 

### Preview:
- The NConvert-Bash Gradio WebUi...
![Alternative text](https://github.com/wiseman-timelord/NConvert-Bash/blob/main/media/gradio-interface.jpg?raw=true)
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
✓ Dir exists: temp
Checking Virtual Env...
✓ Venv valid
Checking NConvert...
✓ NConvert present and executable
Checking PyGObject Symlink...
✓ PyGObject symlink valid
Checking Packages...
✓ Venv valid
✓ Libraries installed
✓ Dependencies installed
✓ All checks passed

--------------------------------------------------------------------------------
Press Enter to continue...

```

## Requirements:
- Linux - It is intended to be compatible with Ubuntu 22.04-25.04.
- [NConvert](https://www.xnview.com/en/nconvert) - ~500 image formats supported (installed by installer).
- Python - Compatible with versions 3.9-3.13, while NConvert-Bash v1.00 if Python 3.8-3.12. Installer will install required Libraries.

### Notation
- De-Confustion... Meaning 1: "Bash" - a `*.sh` Linux Bash file. Meaning 2: "Bash" - Bashful actions done upon/with something hammerlike. 
- If you want others among the ~500 possible formats, then you will need to manually edit ".\scripts\temporary.py".
- Thanks to, DeepSeek, Grok, Claude, Gpt, for assistance in manually prompted programming. 
- Thanks to [XnView Software](https://www.xnview.com/en/) for, creating and hosting, [NConvert](https://www.xnview.com/en/nconvert/), the command-line tool behind my frontend.
- NConvert-Bash is the Lunux version of [NConvert-Batch](https://github.com/wiseman-timelord/NConvert-Batch).

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
1. Improvement of UI.
2. Idea to add additional tickbox fof "Popup Folder After Conversion".
3. A Json to preserve the parameters of previous session, load on start / save on exit.
4. Merge with NConvert-Batch, make dual mode python scripts, then have bash + batch files for launch with linux/windows argument.
