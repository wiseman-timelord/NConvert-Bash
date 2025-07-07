# Script: `.\launcher.py`

# Imports
import os
import sys
import socket
import webbrowser
from threading import Timer
from scripts.interface import create_gradio_interface

# Define base and workspace directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, 'workspace')
VENV_DIR = os.path.join(BASE_DIR, 'venv')  # Added venv reference

def check_port(port):
    """Check if the specified port is in use."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            return sock.connect_ex(("localhost", port)) == 0
    except Exception:
        return False

def find_available_port(start_port=7860, max_attempts=10):
    """Find an available port starting from start_port."""
    for i in range(max_attempts):
        port = start_port + i
        if not check_port(port):
            return port
    print("Error: No available ports found. Please close other applications and try again.")
    sys.exit(1)

def main():
    """Main entry point for launching the NConvert-Bash program."""
    os.system('clear')
    print("="*80)
    print("NConvert-Bash - Main Program")
    print("="*80)
    
    # Check for root privileges
    if os.geteuid() == 0:
        print("\nWARNING: Running with root privileges may cause browser issues")
        print("Recommendation: Run without sudo for better experience")
        print("If using sudo is required, manually open browser after launch")

    # Verify virtual environment exists
    if not os.path.exists(VENV_DIR):
        print("ERROR: Virtual environment not found. Please run the installer first.")
        sys.exit(1)

    # Create workspace directory
    try:
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        print(f"Workspace directory ready: {WORKSPACE_DIR}")
    except Exception as e:
        print(f"Error creating workspace directory: {e}")
        sys.exit(1)

    # Create Gradio interface
    try:
        demo = create_gradio_interface()
    except Exception as e:
        print(f"Error creating Gradio interface: {e}")
        sys.exit(1)

    # Find available port
    port = find_available_port()
    url = f"http://localhost:{port}"
    print(f"Starting Gradio interface on {url}")

    # Launch Gradio interface
    try:
        demo.launch(
            server_name="localhost",
            server_port=port,
            share=False,
            inbrowser=False,  # Disable automatic browser opening
            show_error=True,
            quiet=False
        )
    except Exception as e:
        print(f"Error launching Gradio interface: {e}")
        print("Please check that the port is available and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()