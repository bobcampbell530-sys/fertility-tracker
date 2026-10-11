"""
Astrology Tab - Birth chart, moon phases, lunar cycle influence.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class AstrologyTab(ttk.Frame):
    """Astrology and lunar influence UI."""

    def __init__(self, parent, astrology_engine, data_manager, calculator=None):
        super().__init__(parent)
        self.astrology = astrology_engine
        self.data = data_manager
        self.calculator = calculator

        self._create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.refresh()

    def _create_widgets(self):
        """Create astrology UI."""
        # Left panel - Birth chart
        left_frame = ttk.LabelFrame(self, text="Your Birth Chart", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.chart_text = tk.Text(left_frame, height=20, font=("Arial", 10), wrap=tk.WORD)
        self.chart_text.pack(fill=tk.BOTH, expand=True)
        self.chart_text.config(state=tk.DISABLED)

        # Right panel - Moon phase
        right_frame = ttk.LabelFrame(self, text="Current Moon Phase", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        self.moon_display = tk.Canvas(right_frame, width=200, height=200)
        self.moon_display.pack(pady=10)

        self.moon_info_text = tk.Text(right_frame, height=10, font=("Arial", 10), wrap=tk.WORD)
        self.moon_info_text.pack(fill=tk.X)
        self.moon_info_text.config(state=tk.DISABLED)

        # Check moon button
        ttk.Button(right_frame, text="Update Moon Phase", command=self._update_moon_display).pack(fill=tk.X, pady=5)

        # Bottom panel - Moon cycle influence
        bottom_frame = ttk.LabelFrame(self, text="Moon & Cycle Alignment", padding=10)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.moon_cycle_text = tk.Text(bottom_frame, height=15, font=("Arial", 10), wrap=tk.WORD)
        self.moon_cycle_text.pack(fill=tk.BOTH, expand=True)
        self.moon_cycle_text.config(state=tk.DISABLED)

        ttk.Button(bottom_frame, text="Generate Moon-Cycle Map",
                  command=self._generate_moon_cycle_map).pack(fill=tk.X, pady=5)

    def refresh(self):
        """Refresh astrology information."""
        self._update_birth_chart()
        self._update_moon_display()

    def _update_birth_chart(self):
        """Update birth chart display."""
        profile = self.data.get_profile()
        birth_date_str = profile.get("birth_date", "")
        birth_time = profile.get("birth_time", "")
        birth_place = profile.get("birth_place", "")

        if not birth_date_str:
            chart_text = (
                "Your Birth Chart\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Enter your birth details in the Profile & Settings tab\n"
                "to see your astrological information.\n\n"
                "What we'll calculate:\n"
                "• Sun sign (based on birth date)\n"
                "• Moon phase at birth\n"
                "• Approximate moon sign at birth\n"
                "• Approximate rising sign (with time)\n"
                "• Seasonal health guidance\n\n"
                "This information helps personalize\n"
                "your nutrition and supplement recommendations."
            )
        else:
            try:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                if birth_time:
                    birth_date = datetime.strptime(f"{birth_date_str} {birth_time}", "%Y-%m-%d %H:%M")

                chart = self.astrology.calculate_birth_chart_basic(birth_date, birth_time, birth_place)
                seasonal = self.astrology.get_seasonal_supplement_guidance(birth_date, datetime.now())

                chart_text = (
                    f"Your Birth Chart\n"
                    f"{'='*50}\n\n"
                    f"🌞 Sun Sign: {chart['sun_sign']['name']} {chart['sun_sign']['symbol']}\n"
                    f"   Element: {chart['sun_sign']['element'].capitalize()}\n"
                    f"   Dates: {chart['sun_sign']['dates']}\n\n"
                    f"🌙 Moon Phase at Birth: {chart['moon_phase_at_birth']['name']}\n"
                    f"   Illumination: {chart['moon_phase_at_birth']['illumination']}%\n"
                    f"   Energy: {chart['moon_phase_at_birth']['energy']}\n"
                    f"   {chart['moon_phase_at_birth']['description']}\n\n"
                    f"⭐ Rising Sign (approx): {chart['rising_sign'] or 'Enter birth time for rising sign'}\n\n"
                    f"📍 Birth Place: {birth_place or 'Not entered'}\n\n"
                    f"{'='*50}\n\n"
                    f"Seasonal Guidance\n"
                    f"{'='*50}\n\n"
                    f"Born in: {seasonal['birth_season'].capitalize()}\n"
                    f"Current season: {seasonal['current_season'].capitalize()}\n"
                    f"Focus: {seasonal['seasonal_guidance'].get('focus', '')}\n\n"
                    f"Seasonal Foods:\n"
                    f"  • {', '.join(seasonal['seasonal_guidance'].get('foods', [])[:4])}\n\n"
                    f"Seasonal Supplements:\n"
                    f"  • {', '.join(seasonal['seasonal_guidance'].get('supplements', [])[:4])}"
                )
            except ValueError:
                chart_text = "Invalid birth date format.\nPlease enter your birth date in YYYY-MM-DD format.\n\nCorrect examples:\n• 1990-06-15\n• 1985-03-22\n• 2001-12-01\n\nYou can enter this in the Profile & Settings tab."

        self.chart_text.config(state=tk.NORMAL)
        self.chart_text.delete(1.0, tk.END)
        self.chart_text.insert(tk.END, chart_text)
        self.chart_text.config(state=tk.DISABLED)

    def _update_moon_display(self):
        """Update current moon phase display."""
        moon = self.astrology.get_moon_phase()

        # Draw moon phase
        self.moon_display.delete("all")

        # Background circle (dark)
        cx, cy, r = 100, 100, 80
        self.moon_display.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#1a1a2e", outline="")

        # Illuminated portion
        illumination = moon["illumination"] / 100

        # Draw illuminated portion
        if illumination > 0.5:
            # Waxing: light on right
            if moon["phase"] in ["waxing_crescent", "waxing_gibbous", "full"]:
                # Simple representation
                arc_start = 90 - (illumination * 180) if moon["phase"] == "waxing_gibbous" else 90
                self.moon_display.create_arc(cx-r, cy-r, cx+r, cy+r,
                                            start=0, extent=180,
                                            fill="#FFFACD", outline="")
                # Dark portion
                remaining = 180 - (illumination * 180)
                if remaining < 180:
                    self.moon_display.create_arc(cx-r, cy-r, cx+r, cy+r,
                                                start=180, extent=remaining,
                                                fill="#1a1a2e", outline="")
        elif illumination < 0.5:
            # Waning or crescent
            self.moon_display.create_arc(cx-r, cy-r, cx+r, cy+r,
                                        start=180, extent=int(illumination * 360),
                                        fill="#FFFACD", outline="")

        # Simple moon symbol
        moon_symbol = self._get_moon_symbol(moon["phase"])
        self.moon_display.create_text(cx, cy, text=moon_symbol, font=("Arial", 40), fill="white")

        # Update info text
        info_text = (
            f"{moon['name']}\n"
            f"{'='*30}\n\n"
            f"Illumination: {moon['illumination']}%\n"
            f"Day in lunar cycle: {moon['day_in_cycle']}/{moon['total_cycle_days']}\n"
            f"Energy: {moon['energy']}\n\n"
            f"{moon['description']}"
        )

        self.moon_info_text.config(state=tk.NORMAL)
        self.moon_info_text.delete(1.0, tk.END)
        self.moon_info_text.insert(tk.END, info_text)
        self.moon_info_text.config(state=tk.DISABLED)

    def _generate_moon_cycle_map(self):
        """Generate moon-cycle alignment map."""
        history = self.data.get_cycle_history()

        if not history:
            messagebox.showinfo("No Data", "Log your period dates first to see moon-cycle alignment.")
            return

        # Get last period
        sorted_history = sorted(history, key=lambda x: x["start_date"])
        last_start = datetime.strptime(sorted_history[-1]["start_date"], "%Y-%m-%d")

        cycle_map = self.astrology.get_cycle_moon_influence(last_start, self.calculator.avg_cycle_length if hasattr(self, 'calculator') else 28)

        # Actually we need the calculator instance - let me fix this
        # For now, use a default
        cycle_length = 28
        if hasattr(self, 'calculator'):
            cycle_length = self.calculator.avg_cycle_length

        cycle_map = self.astrology.get_cycle_moon_influence(last_start, cycle_length)

        # Generate display text
        output = (
            f"Moon & Cycle Alignment\n"
            f"{'='*60}\n"
            f"Cycle starting: {last_start.strftime('%B %d, %Y')}\n"
            f"Cycle length: {cycle_length} days\n\n"
        )

        # Show key days
        for day_info in cycle_map["daily_influences"]:
            day = day_info["day"]

            # Only show key days to save space
            if day <= 5 or day == day_info.get('day', 14) or day >= cycle_length - 2:
                output += (
                    f"Day {day:2d} | {day_info['cycle_phase']:12s} | "
                    f"{self._get_moon_symbol(day_info['moon_phase'])} "
                    f"{day_info['moon_name']:15s} | "
                    f"{day_info['energy_theme']}\n"
                    f"     {day_info['recommendation']}\n\n"
                )

        # Show full summary
        output += f"\n{'='*60}\n\n"
        output += "Key Moon-Cycle Insights:\n\n"

        # Find days with full moon during period
        full_moon_days = [d for d in cycle_map["daily_influences"]
                         if d["moon_phase"] == "full"]
        period_days = [d for d in cycle_map["daily_influences"]
                      if d["cycle_phase"] == "menstrual"]

        if full_moon_days and period_days:
            full_moon_day = full_moon_days[0]["day"]
            if any(p["day"] == full_moon_day for p in period_days):
                output += "🌕 Full Moon during menstruation:\n"
                output += "  This is a powerful time for emotional release\n"
                output += "  and setting new intentions.\n\n"

        # Show general recommendations
        output += "General Moon-Cycle Practices:\n"
        output += "  🌑 New Moon: Set intentions, start new supplements\n"
        output += "  🌓 First Quarter: Take action, build momentum\n"
        output += "  🌕 Full Moon: Release, celebrate, socialize\n"
        output += "  🌗 Last Quarter: Reflect, forgive, let go\n"
        output += "  🌘 Waning: Rest, prepare, inner work\n"

        self.moon_cycle_text.config(state=tk.NORMAL)
        self.moon_cycle_text.delete(1.0, tk.END)
        self.moon_cycle_text.insert(tk.END, output)
        self.moon_cycle_text.config(state=tk.DISABLED)

    def _get_moon_symbol(self, phase: str) -> str:
        """Get moon symbol for phase."""
        symbols = {
            "new": "🌑",
            "waxing_crescent": "🌒",
            "first_quarter": "🌓",
            "waxing_gibbous": "🌔",
            "full": "🌕",
            "waning_gibbous": "🌖",
            "last_quarter": "🌗",
            "waning_crescent": "🌘",
        }
        return symbols.get(phase, "🌙")
