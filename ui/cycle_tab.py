"""
Cycle Tracking Tab - Log periods, view predictions, track history.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import Optional


class CycleTrackingTab(ttk.Frame):
    """Cycle tracking and history UI."""

    def __init__(self, parent, calculator, data_manager, calendar_view=None):
        super().__init__(parent)
        self.calculator = calculator
        self.data = data_manager
        self.calendar_view = calendar_view

        self._create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.refresh()

    def _create_widgets(self):
        """Create cycle tracking UI."""
        # Left panel - Current cycle info
        left_frame = ttk.LabelFrame(self, text="Current Cycle Status", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.status_text = tk.Text(left_frame, height=12, font=("Arial", 10), wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        self.status_text.config(state=tk.DISABLED)

        # Right panel - Log period
        right_frame = ttk.LabelFrame(self, text="Log Period", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        ttk.Label(right_frame, text="Start Date (YYYY-MM-DD, e.g. 2026-01-15):", foreground="gray").pack(anchor=tk.W, pady=(5, 2))
        self.start_date_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.start_date_var, width=20).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_frame, text="End Date (optional, YYYY-MM-DD, e.g. 2026-01-20):", foreground="gray").pack(anchor=tk.W, pady=(0, 2))
        self.end_date_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.end_date_var, width=20).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_frame, text="Notes (optional):").pack(anchor=tk.W, pady=(0, 2))
        self.notes_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.notes_var, width=20).pack(fill=tk.X, pady=(0, 10))

        ttk.Button(right_frame, text="Log Period", command=self._log_period).pack(fill=tk.X, pady=10)

        # Auto-fill buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Today", command=lambda: self._set_today_start()).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="Yesterday", command=lambda: self._set_yesterday_start()).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        # Bottom panel - Cycle history
        history_frame = ttk.LabelFrame(self, text="Cycle History", padding=10)
        history_frame.pack(fill=tk.X, padx=5, pady=5)

        history_list_frame = ttk.Frame(history_frame)
        history_list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar and listbox
        scrollbar = ttk.Scrollbar(history_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(history_list_frame, yscrollcommand=scrollbar.set,
                                         font=("Arial", 9), height=6)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=self.history_listbox.yview)

        self.history_listbox.bind("<<ListboxSelect>>", self._on_history_select)

        # Delete button
        ttk.Button(history_frame, text="Delete Selected", command=self._delete_entry).pack(fill=tk.X, pady=5)

        # Cycle statistics
        stats_frame = ttk.LabelFrame(self, text="Cycle Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)

        self.stats_text = tk.Text(stats_frame, height=6, font=("Arial", 10), wrap=tk.WORD)
        self.stats_text.pack(fill=tk.X)
        self.stats_text.config(state=tk.DISABLED)

    def refresh(self):
        """Refresh all cycle information."""
        self._update_status()
        self._update_history_list()
        self._update_statistics()

    def _update_status(self):
        """Update current cycle status display."""
        # Set cycle history in calculator
        self.calculator.set_cycle_history(self.data.get_cycle_history())

        cycle_info = self.calculator.calculate_current_cycle_info()

        if not cycle_info:
            status = (
                "No cycle data recorded yet.\n\n"
                "To get started:\n"
                "1. Log your last period start date above (e.g. 2026-01-15)\n"
                "2. The calendar will show predictions\n"
                "3. Track your cycle over time for better predictions\n\n"
                "Tip: The more cycles you track, the more accurate your predictions become."
            )
        else:
            phase_descriptions = {
                "menstrual": "🩸 MENSTRUAL PHASE\nYour period is active. Focus on rest and nourishment.",
                "follicular": "🌱 FOLLICULAR PHASE\nEstrogen is rising. Energy is building.",
                "ovulation": "🌟 OVULATION\nPeak fertility window. Highest energy.",
                "luteal": "🍂 LUTEAL PHASE\nProgesterone dominant. Wind down period.",
            }

            status = (
                f"Last period started: {cycle_info['last_period_start'].strftime('%B %d, %Y')}\n"
                f"{'='*50}\n\n"
                f"{phase_descriptions.get(cycle_info['current_phase'], '')}\n\n"
                f"Day {cycle_info['day_of_cycle']} of {cycle_info['cycle_length']}-day cycle\n"
                f"Days until next period: {cycle_info['days_to_period']}\n\n"
                f"Predicted ovulation: {cycle_info['predicted_ovulation'].strftime('%B %d, %Y')}\n"
                f"Fertile window: {cycle_info['fertile_window']['start'].strftime('%B %d')} - "
                f"{cycle_info['fertile_window']['end'].strftime('%B %d, %Y')}\n\n"
                f"Average cycle length: {self.calculator.avg_cycle_length} days"
            )

        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, status)
        self.status_text.config(state=tk.DISABLED)

    def _update_history_list(self):
        """Update the cycle history listbox."""
        self.history_listbox.delete(0, tk.END)

        history = self.data.get_cycle_history()
        for entry in history:
            start = entry["start_date"]
            end = entry.get("end_date", "")
            notes = entry.get("notes", "")

            start_dt = datetime.strptime(start, "%Y-%m-%d")
            start_str = start_dt.strftime("%b %d, %Y")

            if end:
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                days = (end_dt - start_dt).days + 1
                end_str = end_dt.strftime("%b %d")
            else:
                days = "?"
                end_str = ""

            line = f"{start_str}"
            if end_str:
                line += f" to {end_str}"
            line += f" ({days}d)"
            if notes:
                line += f" - {notes}"

            self.history_listbox.insert(tk.END, line)

    def _update_statistics(self):
        """Update cycle statistics display."""
        history = self.data.get_cycle_history()

        if len(history) < 2:
            stats = (
                "Cycle Statistics\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Periods logged: {len(history)}\n"
                f"Average cycle length: {self.calculator.avg_cycle_length} days\n\n"
                "Log at least 2 periods to see cycle length statistics.\n"
                "The more data you track, the more accurate your predictions become."
            )
        else:
            # Calculate statistics
            dates = []
            for entry in history:
                dates.append(datetime.strptime(entry["start_date"], "%Y-%m-%d"))
            dates.sort()

            lengths = []
            for i in range(1, len(dates)):
                diff = (dates[i] - dates[i - 1]).days
                if 20 <= diff <= 45:
                    lengths.append(diff)

            if lengths:
                avg = sum(lengths) / len(lengths)
                min_len = min(lengths)
                max_len = max(lengths)
                variance = max_len - min_len

                # Check for regularity
                if variance <= 3:
                    regularity = "Very Regular"
                elif variance <= 5:
                    regularity = "Regular"
                elif variance <= 7:
                    regularity = "Somewhat Variable"
                else:
                    regularity = "Variable (consider tracking more)"

                stats = (
                    f"Cycle Statistics\n"
                    f"{'='*40}\n"
                    f"Periods logged: {len(history)}\n"
                    f"Cycle lengths analyzed: {len(lengths)}\n"
                    f"Average: {avg:.1f} days\n"
                    f"Range: {min_len} - {max_len} days\n"
                    f"Variability: {variance} days\n"
                    f"Pattern: {regularity}\n\n"
                    f"Your average cycle length is {self.calculator.avg_cycle_length} days\n"
                    f"Predicted ovulation: ~Day {self.calculator.avg_cycle_length - 14}\n"
                    f"Fertile window: ~Days {max(self.calculator.avg_cycle_length - 19, 6)}-{self.calculator.avg_cycle_length - 13}"
                )
            else:
                stats = (
                    f"Cycle Statistics\n"
                    f"{'='*40}\n"
                    f"Periods logged: {len(history)}\n"
                    f"Valid cycles: 0\n\n"
                    "No valid cycles found (expected 20-45 day intervals).\n"
                    "Double-check your dates and try again."
                )

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)
        self.stats_text.config(state=tk.DISABLED)

    def _log_period(self):
        """Log a new period entry."""
        start = self.start_date_var.get().strip()
        end = self.end_date_var.get().strip()
        notes = self.notes_var.get().strip()

        if not start:
            messagebox.showwarning("Missing Date", "Please enter a start date.")
            return

        # Validate date format
        try:
            datetime.strptime(start, "%Y-%m-%d")
            if end:
                datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.\nCorrect examples:\n• 2026-01-15\n• 2025-12-01\n• 2024-06-30")
            return

        # Save to data
        self.data.add_cycle_entry(start, end, notes)

        # Update calculator
        self.calculator.set_cycle_history(self.data.get_cycle_history())

        # Recalculate average if we have enough data
        if len(self.data.get_cycle_history()) >= 2:
            self._recalculate_average()

        # Clear form
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.notes_var.set("")

        # Update UI
        self.refresh()

        if self.calendar_view:
            self.calendar_view.set_last_period(start)

        messagebox.showinfo("Logged", f"Period logged starting {start}")

    def _recalculate_average(self):
        """Recalculate average cycle length from history."""
        history = self.data.get_cycle_history()
        if len(history) < 2:
            return

        dates = []
        for entry in history:
            dates.append(datetime.strptime(entry["start_date"], "%Y-%m-%d"))
        dates.sort()

        lengths = []
        for i in range(1, len(dates)):
            diff = (dates[i] - dates[i - 1]).days
            if 20 <= diff <= 45:
                lengths.append(diff)

        if lengths:
            new_avg = round(sum(lengths) / len(lengths))
            self.calculator.update_cycle_params(avg_cycle_length=new_avg)
            self.data.set_profile({
                **self.data.get_profile(),
                "average_cycle_length": new_avg,
            })

    def _delete_entry(self):
        """Delete selected cycle entry."""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a cycle entry to delete.")
            return

        index = selection[0]
        if messagebox.askyesno("Confirm Delete", "Delete this cycle entry?"):
            self.data.remove_cycle_entry(index)
            self.calculator.set_cycle_history(self.data.get_cycle_history())

            if self.calendar_view:
                history = self.data.get_cycle_history()
                if history:
                    sorted_history = sorted(history, key=lambda x: x["start_date"])
                    self.calendar_view.set_last_period(sorted_history[-1]["start_date"])
                else:
                    self.calendar_view.set_last_period("")

            self.refresh()

    def _on_history_select(self, event):
        """Handle history listbox selection."""
        pass

    def _set_today_start(self):
        """Set start date to today."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.start_date_var.set(today)

    def _set_yesterday_start(self):
        """Set start date to yesterday."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.start_date_var.set(yesterday)
