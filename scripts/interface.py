# Script: `.\scripts\interface.py`

# Imports
import gradio as gr
import os
from scripts.temporary import ALLOWED_FORMATS, FOLDER_LOCATION, FORMAT_FROM, FORMAT_TO
from scripts.utility import (
    browse_folder, start_conversion, set_folder_location,
    set_format_from, set_format_to, set_delete_files_after
)

def print_status(message, success=True):
    """Print a status message with a checkmark or cross."""
    symbol = "✓" if success else "✗"
    print(f"{symbol} {message}")

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    def on_browse_folder():
        """Handle folder browsing."""
        new_location = browse_folder()
        set_folder_location(new_location)
        return new_location

    def on_format_from_change(new_format):
        """Handle source format change."""
        return set_format_from(new_format)

    def on_format_to_change(new_format):
        """Handle target format change."""
        return set_format_to(new_format)

    def on_delete_change(should_delete):
        """Handle delete checkbox change."""
        return set_delete_files_after(should_delete)

    def on_start_conversion():
        """Handle conversion start."""
        result = start_conversion()
        print_status("Conversion completed" if "Successfully converted" in result else "Conversion encountered errors")
        return result

    def on_exit():
        """Handle program exit with root permission awareness."""
        if os.geteuid() == 0:  # Check if running as root
            print("\nWARNING: Running as root - using safer exit method")
            os._exit(0)  # Immediate exit for root
        else:
            sys.exit(0)  # Normal exit for non-root

    # Create Gradio interface
    with gr.Blocks(title="NConvert-Bash Image Converter", theme=gr.themes.Default()) as demo:
        gr.Markdown("# NConvert-Bash Image Converter")
        gr.Markdown("Convert multiple image files between formats using NConvert.")
        
        with gr.Row():
            folder_location_display = gr.Textbox(
                label="Folder Location",
                value=FOLDER_LOCATION,
                interactive=True,
                scale=4,
                placeholder="Enter folder path or use Browse button"
            )
            browse_button = gr.Button("Browse", scale=1, variant="secondary")
        
        with gr.Row():
            format_from_input = gr.Dropdown(
                label="Convert From",
                choices=ALLOWED_FORMATS,
                value=FORMAT_FROM,
                interactive=True,
                scale=1
            )
            format_to_input = gr.Dropdown(
                label="Convert To",
                choices=ALLOWED_FORMATS,
                value=FORMAT_TO,
                interactive=True,
                scale=1
            )
            delete_files_checkbox = gr.Checkbox(
                label="Delete Original Files After Conversion",
                value=False,
                scale=1
            )
        
        with gr.Row():
            start_button = gr.Button("Start Conversion", variant="primary", scale=4)
            exit_button = gr.Button("Exit Program", variant="stop", scale=1)

        result_output = gr.Textbox(
            label="Conversion Results",
            interactive=False,
            lines=10,
            max_lines=20,
            show_copy_button=True
        )

        # Connect events
        browse_button.click(
            fn=on_browse_folder,
            inputs=None,
            outputs=folder_location_display
        )
        
        folder_location_display.change(
            fn=set_folder_location,
            inputs=folder_location_display,
            outputs=folder_location_display
        )
        
        format_from_input.change(
            fn=on_format_from_change,
            inputs=format_from_input,
            outputs=None
        )
        
        format_to_input.change(
            fn=on_format_to_change,
            inputs=format_to_input,
            outputs=None
        )
        
        delete_files_checkbox.change(
            fn=on_delete_change,
            inputs=delete_files_checkbox,
            outputs=None
        )
        
        start_button.click(
            fn=on_start_conversion,
            inputs=None,
            outputs=result_output
        )
        
        exit_button.click(
            fn=on_exit,
            inputs=None,
            outputs=None
        )

    print_status("Gradio interface created successfully")
    return demo
