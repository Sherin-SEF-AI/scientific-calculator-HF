"""
Hugging Face Spaces deployment script
This is the main entry point for Hugging Face Spaces
"""

import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_interface

# Create the Gradio interface
app = create_interface()

# Launch the application
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


