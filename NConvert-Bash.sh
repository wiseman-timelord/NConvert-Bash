#!/bin/bash

header() {
    echo "================================================================================"
    echo "    NConvert-Bash"
    echo "================================================================================"
}

separator() {
    echo "--------------------------------------------------------------------------------"
}

check_venv() {
    if [ ! -d "venv" ]; then
        echo "ERROR: Virtual environment not found. Please select Install first."
        sleep 3
        return 1
    fi
    return 0
}

activate_venv() {
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
}

deactivate_venv() {
    if command -v deactivate &>/dev/null; then
        deactivate
    fi
}

while true; do
    clear
    header
    printf "\n\n\n\n\n\n"
    printf "    1. Launch Main Program \n\n"
    printf "    2. Install Files/Libraries \n\n"
    printf "    3. Validate Files/Libraries \n"
    printf "\n\n\n\n\n\n"
	separator
    read -p "Selection; Menu Options 1-3, Exit Bash = X: " choice
    case $choice in
        1)
            if check_venv; then
                activate_venv
                venv/bin/python launcher.py
                deactivate_venv
                read -p "Press Enter to continue..."
            fi
            ;;
        2)
            python3 installer.py
            deactivate_venv  # Ensure venv is deactivated after installer
            read -p "Press Enter to continue..."
            ;;
        3)
            if check_venv; then
                activate_venv
                venv/bin/python validation.py
                deactivate_venv
                read -p "Press Enter to continue..."
            fi
            ;;
        X|x)
            exit 0
            ;;
        *)
            echo "Invalid selection. Please choose 1, 2, 3, or X."
            sleep 1
            ;;
    esac
done