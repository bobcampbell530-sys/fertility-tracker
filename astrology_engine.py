"""
Astrology Engine - Calculates sun signs, moon phases, and lunar influence on cycles.
All calculations are done locally with no external dependencies.
"""

from datetime import datetime as dt, date as d, timedelta
from typing import Optional


class AstrologyEngine:
    """Core astrology calculation engine."""

    # Zodiac signs with date ranges
    ZODIAC_SIGNS = [
        ("Capricorn", d(2000, 12, 22), d(2001, 1, 19), "♑"),
        ("Aquarius", d(2001, 1, 20), d(2001, 2, 18), "♒"),
        ("Pisces", d(2001, 2, 19), d(2001, 3, 20), "♓"),
        ("Aries", d(2001, 3, 21), d(2001, 4, 19), "♈"),
        ("Taurus", d(2001, 4, 20), d(2001, 5, 20), "♉"),
        ("Gemini", d(2001, 5, 21), d(2001, 6, 20), "♊"),
        ("Cancer", d(2001, 6, 21), d(2001, 7, 22), "♋"),
        ("Leo", d(2001, 7, 23), d(2001, 8, 22), "♌"),
        ("Virgo", d(2001, 8, 23), d(2001, 9, 22), "♍"),
        ("Libra", d(2001, 9, 23), d(2001, 10, 22), "♎"),
        ("Scorpio", d(2001, 10, 23), d(2001, 11, 21), "♏"),
        ("Sagittarius", d(2001, 11, 22), d(2001, 12, 21), "♐"),
    ]

    # Moon phase meanings for cycle guidance
    MOON_PHASES = {
        "new": {"name": "New Moon", "energy": "setting_intentions", "description": "New beginnings, planting seeds, setting intentions"},
        "waxing_crescent": {"name": "Waxing Crescent", "energy": "building", "description": "Building momentum, taking small actions"},
        "first_quarter": {"name": "First Quarter", "energy": "action", "description": "Taking action, overcoming obstacles, building strength"},
        "waxing_gibbous": {"name": "Waxing Gibbous", "energy": "refining", "description": "Refining plans, adjusting, preparing for peak"},
        "full": {"name": "Full Moon", "energy": "release", "description": "Peak energy, release, culmination, heightened emotions"},
        "waning_gibbous": {"name": "Waning Gibbous", "energy": "gratitude", "description": "Gratitude, sharing wisdom, gentle release"},
        "last_quarter": {"name": "Last Quarter", "energy": "reflection", "description": "Reflection, release what no longer serves, forgiveness"},
        "waning_crescent": {"name": "Waning Crescent", "energy": "rest", "description": "Rest, inner work, surrender, preparation"},
    }

    # Elemental associations for supplements/food
    ELEMENT_PROPERTIES = {
        "fire": {"traits": ["energizing", "passionate", "transforming"],
                "foods": ["spicy foods", "warming spices", "red meats"],
                "supplements": ["B-complex", "iron", "creatine"]},
        "earth": {"traits": ["nourishing", "grounding", "stabilizing"],
                  "foods": ["root vegetables", "whole grains", "protein"],
                  "supplements": ["minerals", "magnesium", "zinc"]},
        "air": {"traits": ["mental_clarity", "communicative", "light"],
                "foods": ["leafy greens", "fresh fruits", "light meals"],
                "supplements": ["omega-3", "ginkgo", "vitamin C"]},
        "water": {"traits": ["emotional", "intuitive", "flowing"],
                  "foods": ["sea vegetables", "fatty fish", "bone broths"],
                  "supplements": ["omega-3", "kelp", "collagen"]},
    }

    # Moon phase influence on menstrual cycle
    MOON_CYCLE_INFLUENCE = {
        "new_moon_phase": {"menstrual_support": "intention setting, journaling, rest",
                          "best_for": ["starting new supplements", "setting health intentions"]},
        "full_moon_phase": {"menstrual_support": "emotional release, warm baths, gentle movement",
                           "best_for": ["herbal teas", "social connection", "energy work"]},
        "first_quarter_moon": {"menstrual_support": "active movement, strength building",
                              "best_for": ["starting new exercise routines", "meal prep"]},
        "last_quarter_moon": {"menstrual_support": "rest, reflection, self-care",
                             "best_for": ["detox protocols", "deep rest"]},
    }

    def __init__(self):
        pass

    def get_sun_sign(self, birth_date: dt) -> dict:
        """Calculate sun sign from birth date."""
        month = birth_date.month
        day = birth_date.day

        for sign_name, start_date, end_date, symbol in self.ZODIAC_SIGNS:
            # Handle sign boundaries
            if sign_name == "Capricorn":
                if (month == 12 and day >= 22) or (month == 1 and day <= 19):
                    return self._make_sign_info(sign_name, symbol, "earth")
            elif (start_date.month < month or
                  (start_date.month == month and start_date.day <= day)):
                if sign_name == "Sagittarius":
                    if month == 11 or (month == 12 and day <= 21):
                        return self._make_sign_info(sign_name, symbol, "fire")
                elif month < end_date.month or (month == end_date.month and day <= end_date.day):
                    element = self._get_element(sign_name)
                    return self._make_sign_info(sign_name, symbol, element)

        # Fallback (shouldn't happen)
        return {"name": "Capricorn", "symbol": "♑", "element": "earth", "dates": "Dec 22 - Jan 19"}

    def get_moon_phase(self, date: Optional[dt] = None) -> dict:
        """
        Calculate moon phase for a given date using astronomical algorithm.
        Based on the synodic month (29.53059 days).
        """
        if date is None:
            date = dt.now()

        # Known new moon: January 6, 2000 at 18:14 UTC (approximate reference)
        known_new_moon = dt(2000, 1, 6, 18, 14)
        synodic_month = 29.53058867  # days

        days_since_known = (date - known_new_moon).total_seconds() / 86400
        cycles_since = days_since_known / synodic_month
        fractional_cycle = cycles_since - int(cycles_since)

        # Convert to phase (0 = new moon)
        phase_angle = fractional_cycle * 360
        phase_day = fractional_cycle * synodic_month

        if phase_day < 1.845:
            phase = "new"
        elif phase_day < 5.536:
            phase = "waxing_crescent"
        elif phase_day < 9.227:
            phase = "first_quarter"
        elif phase_day < 12.918:
            phase = "waxing_gibbous"
        elif phase_day < 16.609:
            phase = "full"
        elif phase_day < 20.300:
            phase = "waning_gibbous"
        elif phase_day < 23.991:
            phase = "last_quarter"
        elif phase_day < 27.682:
            phase = "waning_crescent"
        else:
            phase = "new"

        illumination = self._calculate_illumination(fractional_cycle)

        return {
            "phase": phase,
            "name": self.MOON_PHASES[phase]["name"],
            "energy": self.MOON_PHASES[phase]["energy"],
            "description": self.MOON_PHASES[phase]["description"],
            "illumination": round(illumination, 1),  # 0-100%
            "day_in_cycle": round(phase_day, 1),
            "total_cycle_days": synodic_month,
        }

    def get_moon_phase_for_date(self, date: dt) -> str:
        """Return just the moon phase string for a date."""
        return self.get_moon_phase(date)["phase"]

    def calculate_birth_chart_basic(self, birth_date: dt,
                                    birth_time: Optional[str] = None,
                                    birth_place: Optional[str] = None) -> dict:
        """
        Create a basic birth chart with sun sign, moon sign, and rising sign (approximate).
        """
        sun_sign = self.get_sun_sign(birth_date)

        # Moon sign approximation (moon moves ~12-13 degrees/day through zodiac)
        # More precise calculation would require ephemeris data
        moon_phase = self.get_moon_phase(birth_date)

        # Approximate moon sign based on day of lunar cycle
        # Moon is in a new sign roughly every 2.38 days
        moon_sign_approx = self._approximate_moon_sign(birth_date)

        # Rising sign approximation (requires time)
        rising_sign = None
        if birth_time:
            rising_sign = self._approximate_rising_sign(birth_date, birth_time)

        return {
            "sun_sign": sun_sign,
            "moon_phase_at_birth": moon_phase,
            "moon_sign_approx": moon_sign_approx,
            "rising_sign": rising_sign,
            "birth_place": birth_place,
        }

    def get_cycle_moon_influence(self, cycle_start_date: dt,
                                cycle_length: int = 28) -> dict:
        """
        Map moon phases across a menstrual cycle.
        Shows how lunar energy aligns with cycle phases.
        """
        moon_influences = []

        for day in range(1, cycle_length + 1):
            current_date = cycle_start_date + timedelta(days=day - 1)
            moon = self.get_moon_phase(current_date)

            phase = self._get_cycle_phase_for_day(day, cycle_length)

            moon_influences.append({
                "day": day,
                "date": current_date.strftime("%Y-%m-%d"),
                "cycle_phase": phase,
                "moon_phase": moon["phase"],
                "moon_name": moon["name"],
                "illumination": moon["illumination"],
                "energy_theme": moon["energy"],
                "recommendation": self._get_moon_cycle_recommendation(phase, moon["phase"]),
            })

        return {
            "cycle_start": cycle_start_date,
            "cycle_length": cycle_length,
            "daily_influences": moon_influences,
        }

    def get_seasonal_supplement_guidance(self, birth_date: dt, current_date: dt) -> dict:
        """
        Provide seasonal health guidance based on birth season and current season.
        """
        month = birth_date.month
        current_month = current_date.month

        # Determine seasons
        seasons = {
            "winter": [12, 1, 2],
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "fall": [9, 10, 11],
        }

        birth_season = None
        for season, months in seasons.items():
            if month in months:
                birth_season = season
                break

        current_season = None
        for season, months in seasons.items():
            if current_month in months:
                current_season = season
                break

        seasonal_guidance = {
            "winter": {
                "focus": "warming, grounding, immune support",
                "foods": ["bone broths", "root vegetables", "warming spices (ginger, cinnamon)",
                         "fermented foods", "stews"],
                "supplements": ["vitamin D3+K2", "vitamin C", "zinc", "omega-3", "echinacea"],
                "lifestyle": ["warm baths", "gentle yoga", "adequate sleep", "avoid cold exposure"],
            },
            "spring": {
                "focus": "detoxification, renewal, liver support",
                "foods": ["bitter greens (arugula, dandelion)", "sprouts", "fresh vegetables",
                         "lemon water", "green smoothies"],
                "supplements": ["milk thistle", "nac", "magnesium", "b-complex", "prebiotics"],
                "lifestyle": ["increase movement", "spring cleaning energy", "lighter meals"],
            },
            "summer": {
                "focus": "cooling, hydration, anti-inflammatory",
                "foods": ["water-rich fruits (watermelon, berries)", "cooling herbs (mint, basil)",
                         "light salads", "coconut water", "cucumber"],
                "supplements": ["vitamin D (moderate)", "curcumin", "probiotics", "electrolytes"],
                "lifestyle": ["morning sun exposure", "swimming", "cooling practices"],
            },
            "fall": {
                "focus": "lung support, immunity building, transition",
                "foods": ["pumpkin", "apples", "pears", "garlic", "onions", "nutritional yeast"],
                "supplements": ["vitamin D3", "zinc", "vitamin C", "mushroom extracts", "omega-3"],
                "lifestyle": ["warming foods", "grounding activities", "social connection"],
            },
        }

        return {
            "birth_season": birth_season,
            "current_season": current_season,
            "seasonal_guidance": seasonal_guidance.get(current_season, {}),
            "transition_note": (
                f"Born in {birth_season}, currently in {current_season}. "
                f"Focus on {seasonal_guidance.get(current_season, {}).get('focus', 'balance')}"
            ),
        }

    def _make_sign_info(self, name: str, symbol: str, element: str) -> dict:
        return {
            "name": name,
            "symbol": symbol,
            "element": element,
            "dates": self._get_sign_dates(name),
        }

    def _get_element(self, sign_name: str) -> str:
        elements = {
            "Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
            "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
            "Gemini": "air", "Libra": "air", "Aquarius": "air",
            "Cancer": "water", "Scorpio": "water", "Pisces": "water",
        }
        return elements.get(sign_name, "earth")

    def _get_sign_dates(self, name: str) -> str:
        dates_map = {
            "Capricorn": "Dec 22 - Jan 19", "Aquarius": "Jan 20 - Feb 18",
            "Pisces": "Feb 19 - Mar 20", "Aries": "Mar 21 - Apr 19",
            "Taurus": "Apr 20 - May 20", "Gemini": "May 21 - Jun 20",
            "Cancer": "Jun 21 - Jul 22", "Leo": "Jul 23 - Aug 22",
            "Virgo": "Aug 23 - Sep 22", "Libra": "Sep 23 - Oct 22",
            "Scorpio": "Oct 23 - Nov 21", "Sagittarius": "Nov 22 - Dec 21",
        }
        return dates_map.get(name, "")

    def _calculate_illumination(self, fractional_cycle: float) -> float:
        """Calculate moon illumination percentage (0-100)."""
        # Approximate: illumination follows a sine wave
        import math
        return (1 - math.cos(2 * math.pi * fractional_cycle)) * 50

    def _approximate_moon_sign(self, birth_date: dt) -> str:
        """Approximate moon sign based on lunar cycle position."""
        # Each zodiac sign ~2.38 days
        sign_names = ["Aries", "Taurus", "Gemini", "Cancer",
                      "Leo", "Virgo", "Libra", "Scorpio",
                      "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        # Days since a known new moon
        known_new = dt(2000, 1, 6)
        days_since = (birth_date - known_new).days
        moon_age = days_since % 29.53

        sign_index = int(moon_age / 2.38) % 12
        return sign_names[sign_index]

    def _approximate_rising_sign(self, birth_date: dt,
                                 birth_time: str) -> Optional[str]:
        """
        Very rough rising sign approximation.
        Rising sign changes every ~2 hours.
        This is extremely approximate without exact location and ephemeris.
        """
        try:
            parts = birth_time.split(":")
            hour = int(parts[0])
        except (ValueError, IndexError):
            return None

        sign_names = ["Aries", "Taurus", "Gemini", "Cancer",
                      "Leo", "Virgo", "Libra", "Scorpio",
                      "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        # This is a rough approximation - actual rising sign requires
        # precise astronomical calculation
        sun_sign_index = self._get_sun_sign_index(birth_date)
        # Rising sign is roughly the sign that was ascending at dawn
        # + adjustment for birth hour
        rising_offset = (hour - 6) // 2  # 6 AM = sunrise approximation
        rising_index = (sun_sign_index + rising_offset) % 12

        return sign_names[rising_index]

    def _get_sun_sign_index(self, birth_date: dt) -> int:
        sign_names = ["Aries", "Taurus", "Gemini", "Cancer",
                      "Leo", "Virgo", "Libra", "Scorpio",
                      "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sun = self.get_sun_sign(birth_date)
        return sign_names.index(sun["name"])

    def _get_cycle_phase_for_day(self, day: int, cycle_length: int) -> str:
        """Determine menstrual cycle phase from day number."""
        ovulation_day = cycle_length - 14
        if ovulation_day < 7:
            ovulation_day = 7

        if day <= 5:
            return "menstrual"
        elif day < ovulation_day:
            return "follicular"
        elif day == ovulation_day:
            return "ovulation"
        else:
            return "luteal"

    def _get_moon_cycle_recommendation(self, cycle_phase: str, moon_phase: str) -> str:
        """Get recommendation based on combination of cycle phase and moon phase."""
        recommendations = {
            ("menstrual", "new"): "Rest and reset. Set intentions for your new cycle.",
            ("menstrual", "full"): "Extra rest. Honor the peak lunar energy during bleeding.",
            ("menstrual", "first_quarter"): "Gentle movement. Start with light stretching.",
            ("menstrual", "last_quarter"): "Inner reflection. Journaling and self-care.",
            ("follicular", "waxing_crescent"): "Rising energy. Start new projects.",
            ("follicular", "first_quarter"): "Building strength. Good time for exercise.",
            ("follicular", "waxing_gibbous"): "Refining plans. Nourish and prepare.",
            ("follicular", "new"): "New beginnings. Set health goals.",
            ("ovulation", "full"): "Peak energy. Celebrate and connect. High fertility window.",
            ("ovulation", "waxing_gibbous"): "Approaching peak. Optimize nutrition.",
            ("luteal", "waning_gibbous"): "Graceful transition. Begin wind-down routine.",
            ("luteal", "last_quarter"): "Release what no longer serves. Self-care focus.",
            ("luteal", "waning_crescent"): "Deep rest. Prepare for new cycle.",
            ("luteal", "new"): "Inner work. Meditation and journaling.",
        }
        key = (cycle_phase, moon_phase)
        return recommendations.get(key, "Follow your body's natural rhythm.")
