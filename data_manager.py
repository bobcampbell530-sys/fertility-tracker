"""
Data Manager - Persists user data to JSON files.
Handles woman's profile, birth data, cycle history, and preferences.
"""

import json
import os
from datetime import datetime
from typing import Optional


DEFAULT_CONFIG = {
    "profile": {
        "name": "",
        "birth_date": "",
        "birth_time": "",
        "birth_timezone": "",
        "birth_place": "",
        "average_cycle_length": 28,
        "average_period_length": 5,
    },
    "cycle_history": [],  # List of dicts: {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "notes": ""}
    "supplement_preferences": {
        "tier1": ["omega3", "vitamin_d3k2", "magnesium", "b_complex"],
        "tier2": ["ubiquinol", "nac", "curcumin", "prebiotics"],
        "tier3": [],
    },
    "goals": {
        "trying_to_conceive": False,
        "avoiding_pregnancy": False,
        "general_wellness": True,
    },
    "diet_preferences": {
        "vegetarian": False,
        "vegan": False,
        "gluten_free": False,
        "dairy_free": False,
        "low_glycemic": True,
    },
}


class DataManager:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.expanduser("~"), ".fertility_tracker_data")
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.data_file = os.path.join(data_dir, "fertility_tracker.json")
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                # Ensure all default keys exist (migration safety)
                for key, default_val in DEFAULT_CONFIG.items():
                    if key not in data:
                        data[key] = default_val
                    elif isinstance(default_val, dict):
                        for sub_key, sub_default in default_val.items():
                            if sub_key not in data[key]:
                                data[key][sub_key] = sub_default
                return data
            except (json.JSONDecodeError, IOError):
                return json.loads(json.dumps(DEFAULT_CONFIG))
        return json.loads(json.dumps(DEFAULT_CONFIG))

    def save(self):
        with open(self.data_file, "w") as f:
            json.dump(self._data, f, indent=2)

    # ---- Profile ----

    def get_profile(self) -> dict:
        return self._data["profile"]

    def set_profile(self, profile: dict):
        for key, value in profile.items():
            self._data["profile"][key] = value
        self.save()

    def get_birth_datetime(self) -> Optional[datetime]:
        bd = self._data["profile"].get("birth_date")
        bt = self._data["profile"].get("birth_time")
        if not bd:
            return None
        try:
            if bt:
                return datetime.strptime(f"{bd} {bt}", "%Y-%m-%d %H:%M")
            return datetime.strptime(bd, "%Y-%m-%d")
        except ValueError:
            return None

    # ---- Cycle History ----

    def get_cycle_history(self) -> list:
        return self._data["cycle_history"]

    def add_cycle_entry(self, start_date: str, end_date: str = "", notes: str = ""):
        entry = {"start_date": start_date, "end_date": end_date, "notes": notes}
        self._data["cycle_history"].append(entry)
        self._data["cycle_history"].sort(key=lambda x: x["start_date"])
        self.save()

    def remove_cycle_entry(self, index: int):
        if 0 <= index < len(self._data["cycle_history"]):
            self._data["cycle_history"].pop(index)
            self.save()

    def get_recent_cycles(self, count: int = 6) -> list:
        return self._data["cycle_history"][-count:]

    # ---- Preferences ----

    def get_supplement_preferences(self) -> dict:
        return self._data["supplement_preferences"]

    def set_supplement_preferences(self, prefs: dict):
        self._data["supplement_preferences"] = prefs
        self.save()

    def get_goals(self) -> dict:
        return self._data["goals"]

    def set_goals(self, goals: dict):
        self._data["goals"] = goals
        self.save()

    def get_diet_preferences(self) -> dict:
        return self._data["diet_preferences"]

    def set_diet_preferences(self, prefs: dict):
        self._data["diet_preferences"] = prefs
        self.save()
