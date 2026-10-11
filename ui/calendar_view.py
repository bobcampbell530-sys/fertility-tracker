"""
Calendar View - Monthly calendar showing cycle phases, fertility windows, and moon phases.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import Optional


# Color scheme
COLORS = {
    "menstrual": "#FFB6C1",       # Light pink
    "follicular": "#98FB98",       # Pale green
    "ovulation": "#FFD700",        # Gold
    "luteal": "#DDA0DD",           # Plum
    "fertile_high": "#FF6B6B",     # Red for high fertility
    "fertile_peak": "#FF0000",     # Dark red for peak
    "background": "#FAFAFA",
    "header_bg": "#4A90D9",
    "header_fg": "white",
    "period_bg": "#FFB6C1",
    "fertile_bg": "#FFB3B3",
    "moon_new": "#333333",
    "moon_full": "#FFFACD",
}

MOON_SYMBOLS = {
    "new": "🌑",
    "waxing_crescent": "🌒",
    "first_quarter": "🌓",
    "waxing_gibbous": "🌔",
    "full": "🌕",
    "waning_gibbous": "🌖",
    "last_quarter": "🌗",
    "waning_crescent": "🌘",
}


class CalendarView(tk.Frame):
    """Monthly calendar view with cycle and fertility information."""

    def __init__(self, parent, calculator, astrology_engine, data_manager):
        super().__init__(parent)
        self.calculator = calculator
        self.astrology = astrology_engine
        self.data = data_manager
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.last_period_start = None

        self._create_widgets()
        self._load_last_period()
        self.pack(fill=tk.BOTH, expand=True)  # Pack into parent frame
        self.refresh()

    def _create_widgets(self):
        """Create calendar UI widgets."""
        # Navigation header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prev_btn = ttk.Button(header_frame, text="◀ Prev", command=self._prev_month)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.month_label = ttk.Label(header_frame, text="", font=("Arial", 14, "bold"))
        self.month_label.pack(side=tk.LEFT, expand=True)

        self.next_btn = ttk.Button(header_frame, text="Next ▶", command=self._next_month)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Legend
        legend_frame = ttk.Frame(self)
        legend_frame.pack(fill=tk.X, padx=5, pady=2)

        legend_items = [
            ("🩸 Period", COLORS["menstrual"]),
            ("🟢 Fertile", COLORS["fertile_high"]),
            ("🔴 Peak", COLORS["fertile_peak"]),
            ("🌑 New Moon", COLORS["moon_new"]),
            ("🌕 Full Moon", COLORS["moon_full"]),
        ]

        for text, color in legend_items:
            item = ttk.Frame(legend_frame)
            item.pack(side=tk.LEFT, padx=5)

            swatch = tk.Canvas(item, width=12, height=12, bg=color, highlightthickness=1, highlightbackground="black")
            swatch.pack(side=tk.LEFT)

            ttk.Label(item, text=text).pack(side=tk.LEFT, padx=2)

        # Calendar grid
        self._create_calendar_grid()

        # Info panel
        info_frame = ttk.LabelFrame(self, text="Day Details", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.day_info_text = tk.Text(info_frame, height=8, width=60, font=("Arial", 10))
        self.day_info_text.pack(fill=tk.X)
        self.day_info_text.config(state=tk.DISABLED)

        # Status bar
        self.status_var = tk.StringVar(value="Select a day for details")
        ttk.Label(self, textvariable=self.status_var, font=("Arial", 9), foreground="gray").pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

    def _create_calendar_grid(self):
        """Create the 7-column calendar grid."""
        # Clear existing
        if hasattr(self, "grid_frame"):
            self.grid_frame.destroy()

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = ttk.Label(self.grid_frame, text=day, font=("Arial", 10, "bold"),
                            background=COLORS["header_bg"], foreground=COLORS["header_fg"])
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Day cells
        self.day_buttons = []
        for row in range(1, 8):
            for col in range(7):
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Arial", 9),
                    relief="flat",
                    width=3,
                    height=1,
                    cursor="hand2",
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                btn.configure(
                    bg=COLORS["background"],
                    activebackground="#E0E0E0",
                )
                btn.bind("<Enter>", lambda e, b=btn: self._on_day_hover(b))
                btn.bind("<Button-1>", lambda e, b=btn: self._on_day_click(b))
                self.day_buttons.append(btn)

        # Configure grid weights
        for col in range(7):
            self.grid_frame.columnconfigure(col, weight=1)
        for row in range(1, 8):
            self.grid_frame.rowconfigure(row, weight=1)

    def _load_last_period(self):
        """Load the last period start date from cycle history."""
        history = self.data.get_cycle_history()
        if history:
            sorted_history = sorted(history, key=lambda x: x["start_date"])
            self.last_period_start = datetime.strptime(sorted_history[-1]["start_date"], "%Y-%m-%d")

    def refresh(self):
        """Refresh calendar with current month data."""
        self._render_calendar()

    def _render_calendar(self):
        """Render the calendar grid for current month."""
        first_day = datetime(self.current_year, self.current_month, 1)
        last_day = datetime(self.current_year, self.current_month, 1)

        # Find last day of month
        if self.current_month == 12:
            last_day = datetime(self.current_year, 12, 31)
        else:
            last_day = datetime(self.current_year, self.current_month + 1, 1) - timedelta(days=1)

        # Update header
        self.month_label.config(text=f"{first_day.strftime('%B %Y')}")

        # Calculate offset (Monday = 0)
        start_weekday = (first_day.weekday())  # Monday=0

        # Fill day buttons
        for idx, btn in enumerate(self.day_buttons):
            if idx < 7:  # Header row
                continue

            day_num = idx - 6 - start_weekday

            if day_num < 1 or day_num > last_day.day:
                btn.config(text="", state=tk.DISABLED, bg=COLORS["background"])
                continue

            current_date = datetime(self.current_year, self.current_month, day_num)

            # Get fertility info
            fertility_info = self._get_fertility_for_date(current_date)

            # Get moon phase
            moon_info = self.astrology.get_moon_phase(current_date)

            # Determine day label
            day_text = f"{day_num}"
            if fertility_info["is_period"]:
                day_text = f"{day_num}\n🩸"
            elif fertility_info["is_peak_fertility"]:
                day_text = f"{day_num}\n🔴"
            elif fertility_info["is_fertile"]:
                day_text = f"{day_num}\n🟢"

            # Moon symbol
            moon_symbol = MOON_SYMBOLS.get(moon_info["phase"], "")
            day_text = f"{day_text}\n{moon_symbol}"

            # Set button text and color
            btn.config(
                text=day_text,
                state=tk.NORMAL,
                bg=fertility_info["bg_color"],
                fg=fertility_info["fg_color"],
            )

            # Store date for click handler (Button doesn't have 'tag' option)
            btn._date = current_date

    def _get_fertility_for_date(self, date: datetime) -> dict:
        """Get fertility information for a specific date."""
        # Predict cycle info
        last_period = self.last_period_start
        if not last_period:
            # Use a default based on today
            last_period = datetime.now().replace(day=1) - timedelta(days=28)

        # Find which cycle this date belongs to
        cycle_start = last_period
        while last_period + timedelta(days=self.calculator.avg_cycle_length) < date:
            last_period += timedelta(days=self.calculator.avg_cycle_length)

        cycle = self.calculator.calculate_cycle(cycle_start)
        phase = self.calculator.get_phase_for_date(cycle_start, date)
        day_of_cycle = self.calculator.get_day_of_cycle(cycle_start, date)

        is_fertile = cycle["fertile_window"]["start"] <= date <= cycle["fertile_window"]["end"]
        is_peak = cycle["peak_fertility"]["start"] <= date <= cycle["peak_fertility"]["end"]
        is_period = cycle["menstrual"]["start"] <= date <= cycle["menstrual"]["end"]

        # Determine background color
        if is_period:
            bg_color = COLORS["menstrual"]
            fg_color = "black"
        elif is_peak:
            bg_color = COLORS["fertile_peak"]
            fg_color = "white"
        elif is_fertile:
            bg_color = COLORS["fertile_high"]
            fg_color = "black"
        elif phase == "follicular":
            bg_color = COLORS["follicular"]
            fg_color = "black"
        elif phase == "ovulation":
            bg_color = COLORS["ovulation"]
            fg_color = "black"
        elif phase == "luteal":
            bg_color = COLORS["luteal"]
            fg_color = "black"
        else:
            bg_color = COLORS["background"]
            fg_color = "black"

        return {
            "phase": phase,
            "day_of_cycle": day_of_cycle,
            "is_fertile": is_fertile,
            "is_peak_fertility": is_peak,
            "is_period": is_period,
            "bg_color": bg_color,
            "fg_color": fg_color,
        }

    def _on_day_hover(self, btn):
        """Show brief info on hover."""
        try:
            date = getattr(btn, "_date", None)
            fertility = self._get_fertility_for_date(date)
            moon = self.astrology.get_moon_phase(date)

            phase_names = {
                "menstrual": "Menstrual",
                "follicular": "Follicular",
                "ovulation": "Ovulation",
                "luteal": "Luteal",
            }

            status = (
                f"Day {fertility['day_of_cycle']} | {phase_names.get(fertility['phase'], 'Unknown')} | "
                f"{'🔴 Peak Fertility' if fertility['is_peak_fertility'] else '🟢 Fertile' if fertility['is_fertile'] else 'Not fertile'} | "
                f"{moon['name']}"
            )
            self.status_var.set(status)
        except Exception:
            pass

    def _on_day_click(self, btn):
        """Show detailed info when a day is clicked."""
        try:
            date = getattr(btn, "_date", None)
            self._show_day_details(date)
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def _show_day_details(self, date: datetime):
        """Show detailed information for a clicked day."""
        fertility = self._get_fertility_for_date(date)
        moon = self.astrology.get_moon_phase(date)

        phase_info = fertility.get("phase", "unknown")
        cycle_start = self.last_period_start
        if not cycle_start:
            cycle_start = datetime.now().replace(day=1) - timedelta(days=28)

        cycle_info = self.calculator.calculate_cycle(cycle_start)
        phase_name = {
            "menstrual": "Menstrual Phase",
            "follicular": "Follicular Phase",
            "ovulation": "Ovulation Phase",
            "luteal": "Luteal Phase",
        }.get(phase_name, "Unknown")

        nutrition = None
        from nutrition_advisor import NutritionAdvisor
        goals = self.data.get_goals()
        diet_prefs = self.data.get_diet_preferences()
        advisor = NutritionAdvisor(goals, diet_prefs)
        nutrition = advisor.get_phase_recommendations(phase_name.lower())

        # Get moon-cycle recommendation
        moon_recommendation = self.astrology._get_moon_cycle_recommendation(
            phase_name.lower(), moon["phase"]
        )

        info = (
            f"📅 {date.strftime('%A, %B %d, %Y')}\n"
            f"{'='*50}\n\n"
            f"🔁 Cycle Day: {fertility['day_of_cycle']}\n"
            f"📊 Phase: {phase_name}\n\n"
            f"{'🩸 PERIOD' if fertility['is_period'] else ''}\n"
            f"{'🔴 PEAK FERTILITY' if fertility['is_peak_fertility'] else ''}\n"
            f"{'🟢 FERTILE WINDOW' if fertility['is_fertile'] and not fertility['is_peak_fertility'] else ''}\n"
            f"{'✅ Not fertile' if not fertility['is_fertile'] and not fertility['is_period'] else ''}\n\n"
            f"🌙 Moon: {moon['name']} ({moon['illumination']}% illuminated)\n"
            f"💫 {moon_recommendation}\n\n"
            f"🍽️ Focus: {nutrition.get('focus', '')}\n"
            f"🥗 Recommended: {', '.join(nutrition.get('recommended_foods', [])[:3])}..."
        )

        self.day_info_text.config(state=tk.NORMAL)
        self.day_info_text.delete(1.0, tk.END)
        self.day_info_text.insert(tk.END, info)
        self.day_info_text.config(state=tk.DISABLED)

    def _prev_month(self):
        """Go to previous month."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh()

    def _next_month(self):
        """Go to next month."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.refresh()

    def set_last_period(self, date_str: str):
        """Update the last period start date."""
        if date_str:
            self.last_period_start = datetime.strptime(date_str, "%Y-%m-%d")
        self.refresh()
