"""Main entry point for Bulk File Renamer application."""

import sys
import tkinter as tk
from tkinter import messagebox

from config.constants import APP_NAME, APP_VERSION
from utils.file_utils import setup_logging
from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    try:
        # Set up logging
        setup_logging()
        
        # Create main window
        root = tk.Tk()
        root.withdraw()  # Hide root window
        
        # Create and run the application
        app = MainWindow()
        app.run()
        
    except ImportError as e:
        error_msg = f"Missing required dependency: {e}"
        print(error_msg)
        if 'tkinter' in str(e).lower():
            print("Please install tkinter: pip install tk")
        elif 'PIL' in str(e) or 'Pillow' in str(e):
            print("Please install Pillow: pip install Pillow")
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        print(error_msg)
        
        # Try to show error in GUI if possible
        try:
            messagebox.showerror("Error", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
