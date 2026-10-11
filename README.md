# 🌸 Fertility & Cycle Tracker

A comprehensive fertility tracking application that combines menstrual cycle tracking, astrology, and nutrition planning to help women understand their bodies and optimize their health.

## Features

### 📅 Calendar View
- Monthly calendar showing cycle phases (menstrual, follicular, ovulation, luteal)
- Fertile window indicators (highlighted days)
- Peak fertility markers
- Moon phase symbols on each day
- Click any day for detailed cycle, fertility, and moon information

### 🔁 Cycle Tracking
- Log period start/end dates
- Automatic ovulation prediction (14-day luteal phase method)
- Cycle length statistics and trend analysis
- Historical cycle tracking
- Average cycle length calculation

### 🌙 Astrology
- Sun sign calculation from birth date
- Moon phase calculation (real-time and historical)
- Birth chart basics (sun sign, moon phase at birth, approximate rising sign)
- Moon-cycle alignment mapping
- Seasonal health guidance based on birth season
- Lunar influence recommendations for each cycle phase

### 🍽️ Nutrition & Supplements
- **Food recommendations** by cycle phase:
  - Menstrual: Warm, iron-rich, anti-inflammatory
  - Follicular: Protein, healthy fats, antioxidant-rich
  - Ovulation: Light, energizing, hydration-focused
  - Luteal: Blood sugar stabilizing, magnesium-rich, tryptophan

- **Supplement guidance** by cycle phase (Tier 1-3 system):
  - Tier 1 (Foundation): Omega-3, Vitamin D3+K2, Magnesium, B-Complex
  - Tier 2 (Targeted): Ubiquinol, NAC, Curcumin, Prebiotics, Iron, Zinc, Vitamin C
  - Tier 3 (Advanced): Creatine, Lithium Orotate, Methylene Blue

- Symptom-specific supplement recommendations (cramps, fatigue, PMS, PCOS, etc.)
- Diet preference filtering (vegetarian, vegan, gluten-free, dairy-free)

### 🎯 Goal-Specific Planning

#### Trying to Conceive
- Daily foundational supplements (enhanced for pregnancy prep)
- Optimal timing guide for intercourse
- Lifestyle recommendations (exercise, stress, sleep, environmental)
- Egg quality support (Ubiquinol, folate, etc.)

#### Avoiding Pregnancy
- Fertile window identification
- Cycle fertility map (which days are fertile)
- Natural family planning guidance
- Reliability notes

#### General Wellness
- Cycle-aligned daily nutrition
- Phase-appropriate exercise recommendations
- Seasonal health guidance

## Requirements

- **Python 3.8+**
- **tkinter** (included with standard Python on most systems)

### Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS | ✅ Supported | tkinter included with Python installer |
| Windows | ✅ Supported | tkinter included with Python installer |
| Linux | ✅ Supported | May need to install python3-tk package |

### Linux Installation (if needed)
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

## Installation

### Option 1: Clone and Run
```bash
git clone <repository-url>
cd fertility-tracker
python3 main.py
```

### Option 2: Download Files
1. Download all Python files to a directory
2. Run `python3 main.py`

## Usage

### First Time Setup
1. Open the **Profile & Settings** tab
2. Enter your birth details (date, time, place) for astrology features
3. Set your average cycle length and period length
4. Set your goals (trying to conceive, avoiding pregnancy, or wellness)
5. Set diet preferences if applicable
6. Click **Save Settings**

### Logging a Period
1. Go to **Cycle Tracker** tab
2. Enter start date (and optional end date)
3. Click "Log Period" (or use Today/Yesterday buttons)
4. Calendar automatically updates with predictions

### Using the Calendar
- Navigate months with arrow buttons
- Colors indicate: 🩸 Period, 🟢 Fertile, 🔴 Peak, 🌑🌕 Moon phases
- Hover over any day for quick info
- Click any day for detailed information
- Moon symbols show current lunar phase

### Nutrition Guidance
1. Go to **Nutrition & Supplements** tab
2. Select your current cycle phase
3. View food and supplement recommendations
4. Use symptom selector for specific issues

## Data Storage

All data is stored locally in:
```
~/.fertility_tracker_data/fertility_tracker.json
```

This includes:
- Profile information
- Cycle history
- Goals and preferences
- Diet preferences

## Architecture

```
fertility-tracker/
├── main.py                 # Entry point
├── data_manager.py         # Data persistence (JSON)
├── cycle_calculator.py     # Cycle predictions & phase calculation
├── astrology_engine.py     # Sun sign, moon phase, birth chart
├── nutrition_advisor.py    # Food & supplement recommendations
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Main application window
│   ├── calendar_view.py    # Monthly calendar UI
│   ├── cycle_tab.py        # Cycle tracking UI
│   ├── astrology_tab.py    # Astrology UI
│   ├── nutrition_tab.py    # Nutrition UI
│   └── settings_tab.py     # Settings UI
└── README.md
```

## Cycle Calculation Method

Ovulation is predicted using the **luteal phase constancy** method:
- The luteal phase (post-ovulation) is typically 14 days (range 12-16)
- Ovulation day = Cycle length - 14
- Fertile window = 5 days before ovulation through 1 day after
- Peak fertility = Days 2-3 before ovulation

This method becomes more accurate as more cycle data is logged.

## Moon Phase Calculation

Moon phases are calculated using the synodic month (29.53059 days) from a known new moon reference point. This provides accurate moon phase information without external APIs.

## Health Information

Supplement and nutrition recommendations are based on established nutritional science and systems biology principles, including:
- Omega-3 for inflammation and hormone production
- Vitamin D3+K2 for fertility and immune health
- Magnesium for PMS, cramps, and sleep
- Methylated B-complex (not folic acid) for cell division
- Ubiquinol for egg quality and mitochondrial function
- Iron replenishment during menstruation
- Blood sugar stabilization in luteal phase

**Note:** This is educational information, not medical advice. Always consult your healthcare provider before starting new supplements, especially if you have medical conditions or are taking medications.

## License

MIT License - Free for personal use.

## Acknowledgments

Built with Python's tkinter for cross-platform GUI.
Supplement framework inspired by systems biology nutritional medicine principles.
