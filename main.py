#!/usr/bin/env python3
"""
Fertility & Cycle Tracker
=========================
A comprehensive fertility tracking application that combines:
- Menstrual cycle phase tracking
- Ovulation and fertility predictions  
- Astrological influences (moon phases, birth chart)
- Cycle-aligned nutrition and supplement recommendations

Cross-platform: Mac, Windows, Linux
Requires: Python 3.8+ (tkinter is included with standard Python)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def check_python_version():
    """Verify Python version is 3.8+."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)


def check_tkinter():
    """Verify tkinter is available."""
    try:
        import tkinter
        return True
    except ImportError:
        print("ERROR: tkinter is not installed.")
        print("\nOn Ubuntu/Debian:")
        print("  sudo apt install python3-tk")
        print("\nOn macOS (if using pyenv):")
        print("  brew install tkinter")
        print("\nOn macOS (if using Homebrew Python):")
        print("  brew install tcl-tk")
        print("  Then reinstall Python")
        print("\nOn Windows:")
        print("  tkinter is included with official Python installer")
        sys.exit(1)


def main():
    """Main entry point."""
    check_python_version()
    check_tkinter()

    print("🌸 Fertility & Cycle Tracker")
    print("Loading...")

    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
