#!/bin/bash

header() {
    echo "================================================================================"
    echo "    NConvert-Bash"
    echo "================================================================================"
}

separator() {
    echo "--------------------------------------------------------------------------------"
}

while true; do
    header
    echo "    1. Launch Program"
    echo "    2. Install Files/Libraries"
    echo "    3. Validate Files/Libraries"
    separator
    read -p "Selection; Menu Options 1-3, Exit Bash = X: " choice

    case $choice in
        1)
            python3 launcher.py
            ;;
        2)
            python3 installer.py
            ;;
        3)
            python3 validation.py
            ;;
        X|x)
            exit 0
            ;;
        *)
            echo "Invalid selection. Please choose 1, 2, 3, or X."
            ;;
    esac
done