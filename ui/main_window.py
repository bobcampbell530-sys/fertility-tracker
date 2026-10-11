"""
Main Application Window - Tabbed interface for Fertility Tracker.
Supports Mac, Windows, and Linux via tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from data_manager import DataManager
from cycle_calculator import CycleCalculator
from astrology_engine import AstrologyEngine
from ui.calendar_view import CalendarView
from ui.cycle_tab import CycleTrackingTab
from ui.nutrition_tab import NutritionTab
from ui.settings_tab import SettingsTab


class MainWindow:
    """Main application window with tabbed interface."""

    def __init__(self):
        # Initialize managers
        self.data = DataManager()
        self.calculator = CycleCalculator()
        self.astrology = AstrologyEngine()

        # Update calculator with user data
        profile = self.data.get_profile()
        self.calculator.update_cycle_params(
            avg_cycle_length=int(profile.get("average_cycle_length", 28)),
            period_length=int(profile.get("average_period_length", 5)),
        )
        self.calculator.set_cycle_history(self.data.get_cycle_history())

        # Create main window
        self.root = tk.Tk()
        self.root.title("Fertility & Cycle Tracker")
        # Open at full screen width and height
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{sw}x{sh}")
        self.root.minsize(700, 550)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self._create_menu()
        self._create_tabs()
        self._load_profile()

        # Title bar
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)

        title_label = ttk.Label(title_frame, text="🌸 Fertility & Cycle Tracker",
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)

        ttk.Label(title_frame, text="Cycle-aware nutrition and fertility planning",
                 font=("Arial", 9), foreground="gray").pack(side=tk.RIGHT)

    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Use", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)

    def _create_tabs(self):
        """Create tabbed interface."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab 1: Calendar View
        cal_frame = ttk.Frame(self.notebook)
        self.calendar_view = CalendarView(
            cal_frame, self.calculator, self.astrology, self.data
        )
        self.notebook.add(cal_frame, text="📅 Calendar", sticky="nsew")

        # Tab 2: Cycle Tracking
        cycle_frame = ttk.Frame(self.notebook)
        self.cycle_tab = CycleTrackingTab(
            cycle_frame, self.calculator, self.data, self.calendar_view
        )
        self.notebook.add(cycle_frame, text="🔁 Cycle Tracker", sticky="nsew")

        # Tab 3: Astrology
        astro_frame = ttk.Frame(self.notebook)
        from ui.astrology_tab import AstrologyTab
        self.astrology_tab = AstrologyTab(
            astro_frame, self.astrology, self.data, self.calculator
        )
        self.notebook.add(astro_frame, text="🌙 Astrology", sticky="nsew")

        # Tab 4: Nutrition
        nutrition_frame = ttk.Frame(self.notebook)
        self.nutrition_tab = NutritionTab(
            nutrition_frame, self.data
        )
        self.notebook.add(nutrition_frame, text="🍽️ Nutrition & Supplements", sticky="nsew")

        # Tab 5: Profile & Settings
        settings_frame = ttk.Frame(self.notebook)
        self.settings_tab = SettingsTab(
            settings_frame, self.data, self.calculator
        )
        self.notebook.add(settings_frame, text="⚙️ Profile & Settings", sticky="nsew")

    def _load_profile(self):
        """Load saved profile data into UI."""
        pass  # Individual tabs handle their own loading

    def _open_settings(self):
        """Switch to settings tab."""
        self.notebook.select(4)  # Settings tab is index 4

    def _show_help(self):
        """Show help dialog."""
        help_text = (
            "🌸 Fertility & Cycle Tracker - Help\n\n"
            "Calendar Tab:\n"
            "• View your cycle phases, fertile windows, and moon phases\n"
            "• Click any day for detailed information\n"
            "• Use arrows to navigate months\n\n"
            "Cycle Tracker Tab:\n"
            "• Log your period start/end dates\n"
            "• View cycle predictions and current phase\n"
            "• Track cycle length trends\n\n"
            "Astrology Tab:\n"
            "• View your birth chart basics\n"
            "• See moon phase influence on your cycle\n"
            "• Get seasonal health guidance\n\n"
            "Nutrition Tab:\n"
            "• Get food and supplement recommendations by cycle phase\n"
            "• See fertility-specific guidance\n"
            "• Customize for your diet preferences\n\n"
            "Profile Tab:\n"
            "• Set your birth details (for astrology)\n"
            "• Configure cycle parameters\n"
            "• Set your goals (conceive, avoid, wellness)\n"
            "• Configure diet preferences\n"
        )
        messagebox.showinfo("How to Use", help_text)

    def _show_about(self):
        """Show about dialog."""
        about_text = (
            "🌸 Fertility & Cycle Tracker\n\n"
            "A comprehensive fertility tracking application that combines:\n"
            "• Menstrual cycle phase tracking\n"
            "• Ovulation and fertility predictions\n"
            "• Astrological influences (moon phases, birth chart)\n"
            "• Cycle-aligned nutrition and supplement recommendations\n\n"
            "Supports Mac, Windows, and Linux.\n\n"
            "Requires Python 3.8+ (tkinter is included with standard Python)."
        )
        messagebox.showinfo("About", about_text)

    def run(self):
        """Start the application."""
        self.root.mainloop()
