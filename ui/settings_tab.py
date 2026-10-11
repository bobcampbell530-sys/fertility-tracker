"""
Settings Tab - Profile, goals, diet preferences, and cycle parameters.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class SettingsTab(ttk.Frame):
    """Profile and settings UI."""

    def __init__(self, parent, data_manager, calculator):
        super().__init__(parent)
        self.data = data_manager
        self.calculator = calculator

        self._create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self._load_settings()

    def _create_widgets(self):
        """Create settings UI."""
        # Left panel - Personal Information
        left_frame = ttk.LabelFrame(self, text="Personal Information", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Name
        ttk.Label(left_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5, padx=5)

        # Birth date
        ttk.Label(left_frame, text="Date of Birth:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.birth_date_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.birth_date_var, width=30).grid(row=1, column=1, pady=5, padx=5)
        ttk.Label(left_frame, text="(e.g. 1990-06-15)", foreground="gray").grid(row=1, column=2, sticky=tk.W)

        # Birth time
        ttk.Label(left_frame, text="Time of Birth:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.birth_time_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.birth_time_var, width=30).grid(row=2, column=1, pady=5, padx=5)
        ttk.Label(left_frame, text="(e.g. 14:30, optional)", foreground="gray").grid(row=2, column=2, sticky=tk.W)

        # Birth place
        ttk.Label(left_frame, text="Birth Place:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.birth_place_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.birth_place_var, width=30).grid(row=3, column=1, pady=5, padx=5)
        ttk.Label(left_frame, text="(e.g. Los Angeles, CA)", foreground="gray").grid(row=3, column=2, sticky=tk.W)

        # Separator
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)

        # Cycle Parameters
        ttk.Label(left_frame, text="Cycle Parameters", font=("Arial", 11, "bold")).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Average cycle length
        ttk.Label(left_frame, text="Avg Cycle Length (days):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.cycle_length_var = tk.StringVar(value="28")
        ttk.Spinbox(left_frame, from_=20, to=45, textvariable=self.cycle_length_var,
                   width=10).grid(row=6, column=1, pady=5, padx=5, sticky=tk.W)

        # Period length
        ttk.Label(left_frame, text="Avg Period Length (days):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.period_length_var = tk.StringVar(value="5")
        ttk.Spinbox(left_frame, from_=2, to=10, textvariable=self.period_length_var,
                   width=10).grid(row=7, column=1, pady=5, padx=5, sticky=tk.W)

        # Right panel - Goals
        right_frame = ttk.LabelFrame(self, text="Goals & Preferences", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Goals
        ttk.Label(right_frame, text="Your Goals:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        self.trying_conceive_var = tk.BooleanVar()
        self.avoiding_var = tk.BooleanVar()
        self.wellness_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(right_frame, text="🤰 Trying to Conceive",
                       variable=self.trying_conceive_var).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(right_frame, text="🛡️ Avoiding Pregnancy",
                       variable=self.avoiding_var).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(right_frame, text="💚 General Wellness",
                       variable=self.wellness_var).pack(anchor=tk.W, pady=2)

        # Separator
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Diet Preferences
        ttk.Label(right_frame, text="Diet Preferences:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        self.vegetarian_var = tk.BooleanVar()
        self.vegan_var = tk.BooleanVar()
        self.gluten_free_var = tk.BooleanVar()
        self.dairy_free_var = tk.BooleanVar()
        self.low_glycemic_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(right_frame, text="🥬 Vegetarian",
                       variable=self.vegetarian_var).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(right_frame, text="🌱 Vegan",
                       variable=self.vegan_var).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(right_frame, text="🚫 Gluten Free",
                       variable=self.gluten_free_var).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(right_frame, text="🥛 Dairy Free",
                       variable=self.dairy_free_var).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(right_frame, text="📉 Low Glycemic",
                       variable=self.low_glycemic_var).pack(anchor=tk.W, pady=2)

        # Save button
        save_btn_frame = ttk.Frame(self)
        save_btn_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(save_btn_frame, text="💾 Save Settings", command=self._save_settings,
                  width=20).pack(side=tk.LEFT, padx=5)

        ttk.Button(save_btn_frame, text="📊 View Birth Chart", command=self._view_birth_chart,
                  width=20).pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Settings loaded")
        ttk.Label(self, textvariable=self.status_var, font=("Arial", 9), foreground="gray").pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

    def _load_settings(self):
        """Load saved settings into UI."""
        profile = self.data.get_profile()
        goals = self.data.get_goals()
        diet_prefs = self.data.get_diet_preferences()

        self.name_var.set(profile.get("name", ""))
        self.birth_date_var.set(profile.get("birth_date", ""))
        self.birth_time_var.set(profile.get("birth_time", ""))
        self.birth_place_var.set(profile.get("birth_place", ""))
        self.cycle_length_var.set(str(profile.get("average_cycle_length", 28)))
        self.period_length_var.set(str(profile.get("average_period_length", 5)))

        self.trying_conceive_var.set(goals.get("trying_to_conceive", False))
        self.avoiding_var.set(goals.get("avoiding_pregnancy", False))
        self.wellness_var.set(goals.get("general_wellness", True))

        self.vegetarian_var.set(diet_prefs.get("vegetarian", False))
        self.vegan_var.set(diet_prefs.get("vegan", False))
        self.gluten_free_var.set(diet_prefs.get("gluten_free", False))
        self.dairy_free_var.set(diet_prefs.get("dairy_free", False))
        self.low_glycemic_var.set(diet_prefs.get("low_glycemic", True))

        self.status_var.set("Settings loaded")

    def _save_settings(self):
        """Save settings from UI."""
        # Validate birth date
        birth_date = self.birth_date_var.get().strip()
        if birth_date:
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Birth date must be in YYYY-MM-DD format.\nCorrect examples:\n• 1990-06-15\n• 1985-03-22\n• 2001-12-01")
                return

        # Validate birth time
        birth_time = self.birth_time_var.get().strip()
        if birth_time:
            try:
                datetime.strptime(birth_time, "%H:%M")
            except ValueError:
                messagebox.showerror("Invalid Time", "Birth time must be in HH:MM format (24-hour).")
                return

        # Save profile
        profile = {
            "name": self.name_var.get(),
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_place": self.birth_place_var.get(),
            "average_cycle_length": int(self.cycle_length_var.get()),
            "average_period_length": int(self.period_length_var.get()),
        }
        self.data.set_profile(profile)

        # Save goals
        goals = {
            "trying_to_conceive": self.trying_conceive_var.get(),
            "avoiding_pregnancy": self.avoiding_var.get(),
            "general_wellness": self.wellness_var.get(),
        }
        self.data.set_goals(goals)

        # Save diet preferences
        diet_prefs = {
            "vegetarian": self.vegetarian_var.get(),
            "vegan": self.vegan_var.get(),
            "gluten_free": self.gluten_free_var.get(),
            "dairy_free": self.dairy_free_var.get(),
            "low_glycemic": self.low_glycemic_var.get(),
        }
        self.data.set_diet_preferences(diet_prefs)

        # Update calculator
        self.calculator.update_cycle_params(
            avg_cycle_length=int(self.cycle_length_var.get()),
            period_length=int(self.period_length_var.get()),
        )

        self.status_var.set("Settings saved successfully!")

    def _view_birth_chart(self):
        """Generate and show birth chart."""
        birth_date = self.birth_date_var.get().strip()
        if not birth_date:
            messagebox.showinfo("No Birth Date", "Please enter your birth date first.")
            return

        try:
            birth_dt = datetime.strptime(birth_date, "%Y-%m-%d")
            birth_time = self.birth_time_var.get().strip()
            if birth_time:
                birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")

            from astrology_engine import AstrologyEngine
            astro = AstrologyEngine()
            chart = astro.calculate_birth_chart_basic(birth_dt, birth_time if birth_time else None,
                                                      self.birth_place_var.get())

            moon = astro.get_moon_phase()
            seasonal = astro.get_seasonal_supplement_guidance(birth_dt, datetime.now())

            message = (
                f"Sun Sign: {chart['sun_sign']['name']} {chart['sun_sign']['symbol']}\n"
                f"Element: {chart['sun_sign']['element']}\n\n"
                f"Moon Phase at Birth: {chart['moon_phase_at_birth']['name']}\n"
                f"Current Moon: {moon['name']}\n\n"
                f"Seasonal Focus: {seasonal['seasonal_guidance'].get('focus', '')}"
            )
            messagebox.showinfo("Birth Chart", message)
        except ValueError as e:
            messagebox.showerror("Error", f"Could not generate birth chart: {e}")
