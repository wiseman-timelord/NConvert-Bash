# NConvert-Bash
Status: Alpha (working on: converting a windows frontend/installer for "NConvert", to being a linux version with instead "XnView MP", compatible with ubuntu 24.10)


### Description:
Its a Python Gradio interface for converting MANY common/rare image formats to MANY common/rare image formats, all made possible through `XnView MP` linux native command line capable viewer. The frontend/installer provides a user-friendly menu to set the source folder, input file format, and desired output format. The scripts ensures efficient and seamless conversion and management of image files, making it a practical tool for users needing to process many images in multiple common/rare formats

### Development
1. If possible we will want to use "XnView MP" to as a conversion library for linux, we could silent install it to the "./venv", then run it as a command-line tool, with the file formats setup the same as before, maybe 5 more, that are common and not in the lists already. it would probably be a better idea to keep things linux based. Here is the link `https://www.xnview.com/download.php?file=XnViewMP-linux-x64.tgz`, it will need to go in the installer.
2. We are going to change the file structure....
```
.\NConvert-Bash.sh (bash script, header function, separator function, numbered options menu, "1. Run Main Program", "2. Install Files/Libraries", "3. Files/Libraries Validation".  
.\installer.py (standalone installer script)
.\validation.py (checkse libraries and files are present and correct, standalone)
.\launcher.py (entry point for main program. Should contain "main" function.) 
.\scripts\temporary.py (Should contain all, global variables/constants, global maps/lists/etc.)
.\scripts\interface.py (Should contain, all concise printed terminal text, all gradio code)
.\scripts\utility.py (should contain all code not directly relevant to, main function, global variables/constants, global maps/lists/etc, printed terminal text, gradio code. ie other code goes in utility)
```
3. we would have a menu for the bash script...

```
================================================================================
    NConvert-Bash
================================================================================

    1. Launch Program
 
    2. Install Files/Libraries
 
    3. Validate Files/Libraries

--------------------------------------------------------------------------------
Selection; Menu Options 1-3, Exit Batch = X:

```
4. The individual scripts require re-fractoring and converting.
5. the scripts will require to be checked over, ensuring that traces of windows code are, as possible replaced with relating linux/ubuntu24 compatible code.
