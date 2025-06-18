# NConvert-Bash
Status: Alpha (working on: primary testing)


### Description:
Its a Python Gradio interface for converting MANY common/rare image formats to MANY common/rare image formats, all made possible through `XnView MP` linux native command line capable viewer. The frontend/installer provides a user-friendly menu to set the source folder, input file format, and desired output format. The scripts ensures efficient and seamless conversion and management of image files, making it a practical tool for users needing to process many images in multiple common/rare formats

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

## Requirements:
- Linux - It will be tested on Ubuntu 24.10.
- [NConvert](https://www.xnview.com/en/nconvert) - ~500 image formats supported (installed by installer).
- Python 3.8+ - Compatible with what are now the lower versions of python.
- Python Libraries - Installed from the created `.\requirements.txt`, you can inspect them there if you like.

### File Structure:
- Files in package...
```
.\NConvert-Bash.sh (bash script, "1. Run Main Program", "2. Install Files/Libraries", "3. Files/Libraries Validation".  
.\installer.py (standalone installer script)
.\validation.py (checks libraries and files are present/correct (standalone))
.\launcher.py (entry point for main program. Should contain "main" function.) 
.\scripts\temporary.py (Should contain all, global variables/constants, global maps/lists/etc.)
.\scripts\interface.py (Should contain, all concise printed terminal text, all gradio code)
.\scripts\utility.py (should contain all code not directly relevant to, main function, global variables/constants, global maps/lists/etc, printed terminal text, gradio code. ie other code goes in utility)
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
