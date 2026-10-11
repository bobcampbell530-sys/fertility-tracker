"""
Cycle Calculator - Predicts ovulation, fertile windows, and cycle phases.
Uses luteal phase constancy (typically 14 days) and historical cycle data.
"""

from datetime import datetime, timedelta
from typing import Optional


class CycleCalculator:
    """Core cycle calculation engine."""

    # Standard luteal phase is typically 12-16 days, average ~14
    DEFAULT_LUTEAL_PHASE = 14
    MIN_FERTILE_WINDOW_DAYS = 6  # 5 before ovulation + ovulation day

    # Phase names
    PHASE_MENSTRUAL = "menstrual"
    PHASE_FOLLICULAR = "follicular"
    PHASE_OVULATION = "ovulation"
    PHASE_LUTEAL = "luteal"

    def __init__(self, avg_cycle_length: int = 28, avg_luteal_phase: int = 14, period_length: int = 5):
        self.avg_cycle_length = avg_cycle_length
        self.avg_luteal_phase = avg_luteal_phase
        self.period_length = period_length

    def update_cycle_params(self, avg_cycle_length: Optional[int] = None,
                           avg_luteal_phase: Optional[int] = None,
                           period_length: Optional[int] = None):
        """Update parameters from user data."""
        if avg_cycle_length is not None:
            self.avg_cycle_length = avg_cycle_length
        if avg_luteal_phase is not None:
            self.avg_luteal_phase = avg_luteal_phase
        if period_length is not None:
            self.period_length = period_length

    def calculate_cycle(self, cycle_start_date: datetime, cycle_length: Optional[int] = None) -> dict:
        """
        Calculate all phases for a given cycle starting on cycle_start_date.
        Returns dict with all phase dates and metadata.
        """
        cl = cycle_length or self.avg_cycle_length

        ovulation_day = cl - self.avg_luteal_phase  # Day number (1-indexed)
        if ovulation_day < 7:
            ovulation_day = 7  # Minimum sanity check

        menstrual_start = cycle_start_date
        menstrual_end = cycle_start_date + timedelta(days=self.period_length - 1)

        follicular_start = cycle_start_date + timedelta(days=self.period_length)
        follicular_end = cycle_start_date + timedelta(days=ovulation_day - 1)

        ovulation_date = cycle_start_date + timedelta(days=ovulation_day - 1)

        luteal_start = ovulation_date + timedelta(days=1)
        luteal_end = cycle_start_date + timedelta(days=cl - 1)

        fertile_start = cycle_start_date + timedelta(days=max(ovulation_day - 6, 5))
        fertile_end = cycle_start_date + timedelta(days=ovulation_day)

        # Days of peak fertility (most fertile: 1-2 days before ovulation)
        peak_fertility_start = cycle_start_date + timedelta(days=ovulation_day - 3)
        peak_fertility_end = ovulation_date

        return {
            "cycle_start": menstrual_start,
            "cycle_end": luteal_end,
            "menstrual": {
                "start": menstrual_start,
                "end": menstrual_end,
                "days": list(range(1, self.period_length + 1)),
            },
            "follicular": {
                "start": follicular_start,
                "end": follicular_end,
                "days": list(range(self.period_length + 1, ovulation_day)),
            },
            "ovulation": {
                "date": ovulation_date,
                "day": ovulation_day,
            },
            "luteal": {
                "start": luteal_start,
                "end": luteal_end,
                "days": list(range(ovulation_day + 1, cl + 1)),
            },
            "fertile_window": {
                "start": fertile_start,
                "end": fertile_end,
                "days": list(range(max(ovulation_day - 5, 6), ovulation_day + 1)),
            },
            "peak_fertility": {
                "start": peak_fertility_start,
                "end": peak_fertility_end,
            },
            "ovulation_day_number": ovulation_day,
            "cycle_length": cl,
        }

    def get_phase_for_date(self, cycle_start_date: datetime, target_date: datetime,
                          cycle_length: Optional[int] = None) -> str:
        """Determine which phase a given date falls into within a cycle."""
        cycle = self.calculate_cycle(cycle_start_date, cycle_length)

        # Menstrual phase
        if cycle["menstrual"]["start"] <= target_date <= cycle["menstrual"]["end"]:
            return self.PHASE_MENSTRUAL

        # Follicular phase
        if cycle["follicular"]["start"] <= target_date <= cycle["follicular"]["end"]:
            return self.PHASE_FOLLICULAR

        # Ovulation
        if target_date.date() == cycle["ovulation"]["date"].date():
            return self.PHASE_OVULATION

        # Luteal phase
        if cycle["luteal"]["start"] <= target_date <= cycle["luteal"]["end"]:
            return self.PHASE_LUTEAL

        return "unknown"

    def get_day_of_cycle(self, cycle_start_date: datetime, target_date: datetime) -> int:
        """Return day of cycle (1-based) for a given date."""
        delta = (target_date.date() - cycle_start_date.date()).days
        return max(1, delta + 1)

    def predict_next_periods(self, last_n: int = 6) -> list:
        """
        Predict next 3 period start dates based on recent cycle history.
        Uses average of last N cycles.
        """
        history = []
        for entry in self._cycle_history:
            start = datetime.strptime(entry["start_date"], "%Y-%m-%d")
            history.append(start)

        if len(history) < 1:
            # Use configured average
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return [today + timedelta(days=self.avg_cycle_length * (i + 1)) for i in range(3)]

        # Calculate cycle lengths
        lengths = []
        for i in range(1, len(history)):
            diff = (history[i] - history[i - 1]).days
            if 20 <= diff <= 45:  # Sanity filter
                lengths.append(diff)

        if lengths:
            avg_length = round(sum(lengths) / len(lengths))
        else:
            avg_length = self.avg_cycle_length

        # Predict from last known period
        last_period = history[-1]
        predictions = []
        for i in range(1, 4):
            predicted = last_period + timedelta(days=avg_length * i)
            predictions.append(predicted)
            # Update for next prediction (allow for variability)
            last_period = predicted

        return predictions

    def calculate_current_cycle_info(self) -> Optional[dict]:
        """
        Analyze cycle history to determine current cycle status.
        Returns info about current/next expected phases.
        """
        history = self._cycle_history
        if not history:
            return None

        # Sort by date
        sorted_history = sorted(history, key=lambda x: x["start_date"])

        # Get last cycle
        last_start = datetime.strptime(sorted_history[-1]["start_date"], "%Y-%m-%d")

        # Recalculate average cycle length
        if len(sorted_history) >= 2:
            lengths = []
            for i in range(1, len(sorted_history)):
                diff = (datetime.strptime(sorted_history[i]["start_date"], "%Y-%m-%d") -
                       datetime.strptime(sorted_history[i - 1]["start_date"], "%Y-%m-%d")).days
                if 20 <= diff <= 45:
                    lengths.append(diff)
            if lengths:
                avg_length = round(sum(lengths) / len(lengths))
                self.update_cycle_params(avg_cycle_length=avg_length)

        # Calculate current cycle
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cycle = self.calculate_cycle(last_start)

        current_phase = self.get_phase_for_date(last_start, today)
        day_of_cycle = self.get_day_of_cycle(last_start, today)

        # Days until next period
        next_period = cycle["cycle_end"] + timedelta(days=1)
        days_to_period = (next_period.date() - today.date()).days

        return {
            "last_period_start": last_start,
            "current_phase": current_phase,
            "day_of_cycle": day_of_cycle,
            "days_to_period": days_to_period,
            "predicted_ovulation": cycle["ovulation"]["date"],
            "fertile_window": {
                "start": cycle["fertile_window"]["start"],
                "end": cycle["fertile_window"]["end"],
            },
            "cycle_length": cycle["cycle_length"],
            "cycle_info": cycle,
        }

    @property
    def _cycle_history(self):
        """Access to cycle history - set via setter in manager integration."""
        return getattr(self, "_history", [])

    def set_cycle_history(self, history: list):
        """Set the cycle history for calculations."""
        self._history = history

    def predict_fertility_for_range(self, start_date: datetime, end_date: datetime,
                                   last_period_start: Optional[datetime] = None) -> list:
        """
        Generate a day-by-day fertility forecast for a date range.
        Returns list of dicts with date, phase, fertility info.
        """
        if last_period_start is None:
            last_period_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - \
                               timedelta(days=self.avg_cycle_length)

        forecasts = []
        current = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        while current <= end_date:
            # Find which cycle this date belongs to
            cycle_num = 0
            test_start = last_period_start
            while True:
                next_start = test_start + timedelta(days=self.avg_cycle_length)
                if current < next_start:
                    break
                test_start = next_start
                cycle_num += 1

            cycle = self.calculate_cycle(test_start)
            phase = self.get_phase_for_date(test_start, current)
            day_of_cycle = self.get_day_of_cycle(test_start, current)

            fertility_level = "none"
            is_fertile = False
            is_peak = False

            if current >= cycle["fertile_window"]["start"] and current <= cycle["fertile_window"]["end"]:
                is_fertile = True
                if current >= cycle["peak_fertility"]["start"] and current <= cycle["peak_fertility"]["end"]:
                    is_peak = True
                    fertility_level = "peak"
                else:
                    fertility_level = "high"

            if phase == self.PHASE_MENSTRUAL:
                fertility_level = "none"

            forecasts.append({
                "date": current,
                "phase": phase,
                "day_of_cycle": day_of_cycle,
                "fertility_level": fertility_level,
                "is_fertile": is_fertile,
                "is_peak_fertility": is_peak,
                "is_period": current >= cycle["menstrual"]["start"] and current <= cycle["menstrual"]["end"],
            })

            current += timedelta(days=1)

        return forecasts
