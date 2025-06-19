# Script: `.\scripts\temporary.py`

# Imports
import os

# Base directory (relative to scripts/ directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Workspace directory for file conversions
WORKSPACE_PATH = os.path.join(BASE_DIR, 'workspace')
# Path to nconvert binary
NCONVERT_PATH = os.path.join(BASE_DIR, 'data', 'NConvert-linux64', 'nconvert')

# Default folder location for conversions
FOLDER_LOCATION = WORKSPACE_PATH
# Default source format
FORMAT_FROM = "PSPIMAGE"
# Default target format
FORMAT_TO = "JPEG"
# Default setting for deleting original files
DELETE_FILES_AFTER = False

# Allowed file formats (uppercase for consistency)
ALLOWED_FORMATS = [
    "JPEG", "PNG", "BMP", "GIF", "TIFF", "HEIF", "WEBP", "SVG", "PSD", "PSPIMAGE",
    "ICO", "TGA", "PCX", "JP2", "EXR"
]

# Conversion progress tracking
FILES_PROCESS_DONE = 0
FILES_PROCESS_TOTAL = 0
