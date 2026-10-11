"""
Nutrition Advisor - Provides food and supplement recommendations based on:
- Current menstrual cycle phase
- Moon phase / astrological influences
- User goals (trying to conceive, avoiding pregnancy, general wellness)
- Diet preferences
"""

from typing import Optional


class NutritionAdvisor:
    """Cycle-aware nutrition and supplement guidance engine."""

    # Supplement database with cycle-phase recommendations
    SUPPLEMENTS = {
        # Tier 1 - Foundation
        "omega3": {
            "name": "Omega-3 (EPA/DHA)",
            "tier": 1,
            "dosage": "1,500-3,000mg combined EPA+DHA daily",
            "forms": ["fish oil", "krill oil", "algae oil (vegan)"],
            "cycle_phase": {
                "menstrual": {"priority": "high", "reason": "Anti-inflammatory, reduces cramping and pain"},
                "follicular": {"priority": "high", "reason": "Supports egg development and hormone production"},
                "ovulation": {"priority": "medium", "reason": "Maintains hormonal balance"},
                "luteal": {"priority": "medium", "reason": "Helps with PMS and mood stabilization"},
            },
            "for_pregnancy": "Critical for fetal brain development. Increase to 2,000-3,000mg when trying to conceive.",
            "for_avoidance": "No impact on fertility when taken normally.",
            "cautions": "Must be fresh (rancid = pro-inflammatory). Take with food.",
        },
        "vitamin_d3k2": {
            "name": "Vitamin D3 + K2",
            "tier": 1,
            "dosage": "D3: 2,000-5,000 IU daily | K2 (MK-7): 100-200mcg daily",
            "forms": ["D3 drops or capsules", "combined D3+K2 supplements"],
            "cycle_phase": {
                "menstrual": {"priority": "high", "reason": "Vitamin D receptors in uterus support implantation"},
                "follicular": {"priority": "high", "reason": "Essential for follicle development and egg quality"},
                "ovulation": {"priority": "high", "reason": "Supports ovulation and hormone production"},
                "luteal": {"priority": "medium", "reason": "Supports progesterone production"},
            },
            "for_pregnancy": "Target blood level 50-80 ng/mL. Critical for healthy pregnancy.",
            "for_avoidance": "No impact. General health maintenance.",
            "cautions": "Test blood levels. Take K2 with D3 for proper calcium metabolism.",
        },
        "magnesium": {
            "name": "Magnesium",
            "tier": 1,
            "dosage": "300-400mg daily",
            "forms": {
                "best_general": "Magnesium Glycinate (best absorbed, gentle on stomach)",
                "for_cramps": "Magnesium Glycinate or Citrate",
                "for_sleep": "Magnesium Glycinate",
                "for_energy": "Magnesium Malate",
                "for_fertility": "Magnesium Taurate",
            },
            "cycle_phase": {
                "menstrual": {"priority": "high", "reason": "Reduces cramping, relaxes uterine muscles, eases pain"},
                "follicular": {"priority": "medium", "reason": "Supports energy and enzyme function"},
                "ovulation": {"priority": "medium", "reason": "Hormone regulation"},
                "luteal": {"priority": "high", "reason": "Reduces PMS, bloating, mood swings, supports progesterone"},
            },
            "for_pregnancy": "Essential. Helps prevent preterm labor and supports fetal bone development.",
            "for_avoidance": "No impact on fertility.",
            "cautions": "Space from calcium and zinc by 2-4 hours. Start with lower dose.",
        },
        "b_complex": {
            "name": "Methylated B-Complex",
            "tier": 1,
            "dosage": "As directed (look for methylated forms: methylfolate, methylcobalamin)",
            "forms": ["Methylfolate (not folic acid)", "Methylcobalamin (B12)", "P-5-P (B6)"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Energy support during bleeding"},
                "follicular": {"priority": "high", "reason": "Essential for cell division and egg development"},
                "ovulation": {"priority": "high", "reason": "B6 supports progesterone production"},
                "luteal": {"priority": "high", "reason": "B6 reduces PMS and mood symptoms"},
            },
            "for_pregnancy": "CRITICAL: Methylfolate 400-800mcg daily before conception and during pregnancy prevents neural tube defects.",
            "for_avoidance": "No impact. General health.",
            "cautions": "Must use METHYLATED forms. Regular folic acid may not be properly converted.",
        },

        # Tier 2 - Targeted
        "ubiquinol": {
            "name": "Ubiquinol (CoQH)",
            "tier": 2,
            "dosage": "200-600mg daily",
            "forms": ["Ubiquinol (reduced, active form - preferred)", "Ubiquinone"],
            "cycle_phase": {
                "menstrual": {"priority": "low", "reason": "General mitochondrial support"},
                "follicular": {"priority": "high", "reason": "CRITICAL for egg quality and mitochondrial function"},
                "ovulation": {"priority": "medium", "reason": "Supports ovulation energy"},
                "luteal": {"priority": "medium", "reason": "Progesterone production support"},
            },
            "for_pregnancy": "May improve egg quality, especially for women 35+. One of the most important fertility supplements.",
            "for_avoidance": "No impact.",
            "cautions": "Ubiquinol form is 3-5x better absorbed than ubiquinone.",
        },
        "nac": {
            "name": "NAC (N-Acetyl Cysteine)",
            "tier": 2,
            "dosage": "600-1,800mg daily",
            "forms": ["NAC capsules or powder"],
            "cycle_phase": {
                "menstrual": {"priority": "low", "reason": "Antioxidant support"},
                "follicular": {"priority": "high", "reason": "Improves insulin sensitivity, supports ovulation"},
                "ovulation": {"priority": "medium", "reason": "Antioxidant protection"},
                "luteal": {"priority": "low", "reason": "Mood support through glutathione"},
            },
            "for_pregnancy": "Shown to improve ovulation in PCOS. May support implantation.",
            "for_avoidance": "No impact.",
            "cautions": "May thin mucus. Stop during implantation window if trying to conceive.",
        },
        "curcumin": {
            "name": "Curcumin",
            "tier": 2,
            "dosage": "500-1,000mg daily",
            "forms": ["with piperine (black pepper)", "mercuradiant", "liposomal"],
            "cycle_phase": {
                "menstrual": {"priority": "high", "reason": "Anti-inflammatory, reduces pain and prostaglandins"},
                "follicular": {"priority": "medium", "reason": "Reduces inflammation"},
                "ovulation": {"priority": "low", "reason": "CAUTION: May affect implantation - consider pausing"},
                "luteal": {"priority": "medium", "reason": "Anti-inflammatory, mood support"},
            },
            "for_pregnancy": "Pause during implantation window (ovulation to expected period). Safe before and after.",
            "for_avoidance": "No impact.",
            "cautions": "Avoid during implantation window. Take with fat for absorption.",
        },
        "prebiotics": {
            "name": "Prebiotics + Probiotics",
            "tier": 2,
            "dosage": "Prebiotics: 5-15g daily | Probiotics: 10-50 billion CFU",
            "forms": ["Fermented foods", "Probiotic capsules", "Prebiotic fiber"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Gut health supports estrogen metabolism"},
                "follicular": {"priority": "medium", "reason": "Healthy microbiome supports hormone balance"},
                "ovulation": {"priority": "medium", "reason": "General immune support"},
                "luteal": {"priority": "medium", "reason": "Gut-brain axis supports mood"},
            },
            "for_pregnancy": "Important for pregnancy microbiome. Probiotics may reduce preterm birth risk.",
            "for_avoidance": "No impact.",
            "cautions": "Microbiome connection to hormone metabolism is well-established.",
        },

        # Tier 3 - Advanced
        "creatine": {
            "name": "Creatine",
            "tier": 3,
            "dosage": "3-5g daily",
            "forms": ["Creatine Monohydrate"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Energy support, may reduce fatigue"},
                "follicular": {"priority": "high", "reason": "Women may benefit more during follicular phase"},
                "ovulation": {"priority": "medium", "reason": "Energy production"},
                "luteal": {"priority": "medium", "reason": "May help with luteal phase fatigue"},
            },
            "for_pregnancy": "Safe in pregnancy, may support fetal brain development.",
            "for_avoidance": "No impact.",
            "cautions": "Stay hydrated. 3-5g daily is sufficient.",
        },
        "lithium_orotate": {
            "name": "Lithium Orotate (low dose)",
            "tier": 3,
            "dosage": "1-5mg elemental lithium daily",
            "forms": ["Lithium Orotate (NOT lithium carbonate)"],
            "cycle_phase": {
                "menstrual": {"priority": "low", "reason": "Mood stabilization"},
                "follicular": {"priority": "medium", "reason": "Neuroprotective"},
                "ovulation": {"priority": "low", "reason": "General"},
                "luteal": {"priority": "high", "reason": "May reduce severe PMS and PMDD"},
            },
            "for_pregnancy": "NOT recommended during pregnancy. Stop when trying to conceive.",
            "for_avoidance": "No impact.",
            "cautions": "Very different from prescription lithium. Low dose orotate form. Consult doctor.",
        },
        "methylene_blue": {
            "name": "Methylene Blue (microdose)",
            "tier": 3,
            "dosage": "0.5-4mg daily",
            "forms": ["Pharmaceutical grade only"],
            "cycle_phase": {
                "menstrual": {"priority": "low", "reason": "Mitochondrial support"},
                "follicular": {"priority": "medium", "reason": "Mitochondrial biogenesis"},
                "ovulation": {"priority": "low", "reason": "General"},
                "luteal": {"priority": "low", "reason": "General"},
            },
            "for_pregnancy": "NOT recommended during pregnancy or when trying to conceive.",
            "for_avoidance": "No impact.",
            "cautions": "⚠️ NEVER combine with SSRIs (Serotonin Syndrome). Pharmaceutical grade only.",
        },

        # Fertility-specific
        "iron": {
            "name": "Iron",
            "tier": 2,
            "dosage": "18-45mg daily (based on ferritin levels)",
            "forms": ["Bisglycinate (gentle)", "Heme iron", "Polysaccharide iron"],
            "cycle_phase": {
                "menstrual": {"priority": "high", "reason": "Replenish iron lost during bleeding"},
                "follicular": {"priority": "medium", "reason": "Maintain stores"},
                "ovulation": {"priority": "low", "reason": "No special need"},
                "luteal": {"priority": "low", "reason": "No special need"},
            },
            "for_pregnancy": "Essential. Target ferritin >50 ng/mL before conception.",
            "for_avoidance": "No impact.",
            "cautions": "Test ferritin first. Take with vitamin C. Space from calcium/zinc/magnesium.",
        },
        "zinc": {
            "name": "Zinc",
            "tier": 2,
            "dosage": "15-30mg daily",
            "forms": ["Picolinate", "Bisglycinate", "Citrate"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Tissue repair"},
                "follicular": {"priority": "high", "reason": "Essential for follicle development and cell division"},
                "ovulation": {"priority": "medium", "reason": "Hormone production"},
                "luteal": {"priority": "medium", "reason": "Progesterone support"},
            },
            "for_pregnancy": "Important for fetal development. 15-30mg daily.",
            "for_avoidance": "No impact.",
            "cautions": "Space from calcium and magnesium by 2-4 hours. Long-term high doses may deplete copper.",
        },
        "vitamin_c": {
            "name": "Vitamin C",
            "tier": 2,
            "dosage": "500-1,000mg daily",
            "forms": ["Ascorbic acid", "Buffered (sodium ascorbate)", "Mineral ascorbate"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Adrenal support, antioxidant"},
                "follicular": {"priority": "medium", "reason": "Antioxidant protection for eggs"},
                "ovulation": {"priority": "medium", "reason": "Antioxidant, supports estrogen metabolism"},
                "luteal": {"priority": "high", "reason": "Supports progesterone production"},
            },
            "for_pregnancy": "Immune support. Keep under 1,000mg to avoid oxalate kidney stones.",
            "for_avoidance": "No impact.",
            "cautions": "⚠️ Keep under 1,000-2,000mg daily to avoid kidney stones from oxalates.",
        },
        "vitamin_e": {
            "name": "Vitamin E",
            "tier": 2,
            "dosage": "200-400 IU daily",
            "forms": ["Natural mixed tocopherols", "Tocotrienols"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Antioxidant, may reduce pain"},
                "follicular": {"priority": "medium", "reason": "Antioxidant protection"},
                "ovulation": {"priority": "medium", "reason": "May improve cervical mucus"},
                "luteal": {"priority": "low", "reason": "General antioxidant"},
            },
            "for_pregnancy": "May improve cervical mucus and support implantation.",
            "for_avoidance": "No impact.",
            "cautions": "Use natural form (d-alpha tocopherol), not synthetic (dl-).",
        },
        "iodine": {
            "name": "Iodine",
            "tier": 2,
            "dosage": "150mcg daily (pre-pregnancy) | 220-250mcg (pregnancy)",
            "forms": ["Kelp", "Potassium iodide"],
            "cycle_phase": {
                "menstrual": {"priority": "medium", "reason": "Thyroid support"},
                "follicular": {"priority": "high", "reason": "Thyroid hormone essential for follicle development"},
                "ovulation": {"priority": "medium", "reason": "Thyroid-hormone balance"},
                "luteal": {"priority": "medium", "reason": "Thyroid support for progesterone"},
            },
            "for_pregnancy": "CRITICAL for fetal brain development. Increase to 220-250mcg when pregnant.",
            "for_avoidance": "No impact.",
            "cautions": "Test first if autoimmune thyroid disease. Balance with selenium.",
        },
    }

    # Food database
    FOODS = {
        "menstrual": {
            "focus": "Warm, nourishing, iron-rich, anti-inflammatory",
            "key_nutrients": ["iron", "magnesium", "vitamin C", "b vitamins", "omega-3"],
            "recommended": [
                "Bone broths (collagen, minerals)",
                "Red meat or liver (heme iron, B vitamins)",
                "Leafy greens (iron, magnesium, folate)",
                "Sweet potatoes (vitamin A, complex carbs)",
                "Beets (iron, folate, blood building)",
                "Cherries (anti-inflammatory, melatonin)",
                "Dark chocolate (magnesium, mood)",
                "Ginger tea (anti-inflammatory, anti-nausea)",
                "Warm stews and soups",
                "Fermented foods (sauerkraut, kimchi - gut health)",
            ],
            "foods_to_avoid": [
                "Cold foods and drinks (slow circulation)",
                "Excess caffeine (constricts blood vessels)",
                "Excess salt (bloating)",
                "Alcohol (liver stress, estrogen metabolism)",
                "Processed foods",
            ],
        },
        "follicular": {
            "focus": "Protein, healthy fats, complex carbs, antioxidant-rich",
            "key_nutrients": ["protein", "omega-3", "zinc", "vitamin E", "antioxidants"],
            "recommended": [
                "Fatty fish (salmon, sardines - omega-3)",
                "Sprouts and microgreens (living foods)",
                "Nuts and seeds (walnuts, flax, pumpkin)",
                "Avocado (healthy fats, vitamin E)",
                "Eggs (choline, protein, B vitamins)",
                "Berries (antioxidants)",
                "Quinoa (complete protein)",
                "Green vegetables (chlorophyll, minerals)",
                "Healthy fats (olive oil, coconut oil)",
                "Lemon water (liver support)",
            ],
            "foods_to_avoid": [
                "Sugar and refined carbs (inflammation)",
                "Trans fats",
                "Excess alcohol",
                "Soy in excess (phytoestrogens may disrupt balance)",
            ],
        },
        "ovulation": {
            "focus": "Light, energizing, vitamin-rich, hydration",
            "key_nutrients": ["vitamin C", "zinc", "antioxidants", "fiber"],
            "recommended": [
                "Fresh fruits (especially citrus for vitamin C)",
                "Raw vegetables with healthy dips",
                "Herbal teas (red raspberry leaf, nettle)",
                "Nuts and seeds (pumpkin, sunflower)",
                "Water-rich foods (cucumber, watermelon)",
                "Garlic and onions (antimicrobial, blood flow)",
                "Leafy salads with olive oil dressing",
                "Green smoothies",
            ],
            "foods_to_avoid": [
                "Heavy, greasy foods",
                "Excess caffeine (may affect cervical mucus)",
                "Alcohol",
                "Processed foods",
            ],
        },
        "luteal": {
            "focus": "Stabilize blood sugar, magnesium-rich, tryptophan, complex carbs",
            "key_nutrients": ["magnesium", "zinc", "vitamin B6", "omega-3", "complex carbs", "tryptophan"],
            "recommended": [
                "Complex carbohydrates (oats, brown rice, quinoa)",
                "Turkey and chicken (tryptophan for serotonin)",
                "Bananas (vitamin B6, potassium)",
                "Nuts and seeds (almonds, pumpkin seeds)",
                "Dark leafy greens (magnesium)",
                "Dark chocolate in moderation (magnesium)",
                "Fatty fish (omega-3 for mood)",
                "Whole grains (stable blood sugar)",
                "Herbal teas (chamomile, spearmint)",
                "Cruciferous vegetables (broccoli, cauliflower - estrogen metabolism)",
            ],
            "foods_to_avoid": [
                "Sugar and sweets (blood sugar crashes worsen mood)",
                "Excess salt (bloating worsens in luteal phase)",
                "Excess caffeine (increases anxiety, breast tenderness)",
                "Alcohol (worsens mood swings)",
                "Processed foods",
            ],
        },
    }

    # Cycle phase descriptions for UI display
    PHASE_DESCRIPTIONS = {
        "menstrual": {
            "name": "Menstrual Phase",
            "days": "Days 1-5",
            "description": "Your body is shedding the uterine lining. Energy is lowest. Focus on rest, nourishment, and reflection.",
            "energy": "🌑 Low - Rest and restore",
            "exercise": "Gentle yoga, walking, stretching",
            "lifestyle": "Inner focus, journaling, early sleep, warm foods",
        },
        "follicular": {
            "name": "Follicular Phase",
            "days": "Days 6-Ovulation",
            "description": "Estrogen is rising. Energy increases. Great time for new projects and social activities.",
            "energy": "🌗 Rising - Energy builds",
            "exercise": "Increase intensity, try new activities, HIIT, strength training",
            "lifestyle": "Socialize, start new projects, creative work, cleansing diets",
        },
        "ovulation": {
            "name": "Ovulation Phase",
            "days": "~Day 14 (varies)",
            "description": "Peak estrogen and LH surge. Highest energy and social confidence. Peak fertility window.",
            "energy": "☀️ Peak - High energy and confidence",
            "exercise": "Peak performance activities, team sports, dance",
            "lifestyle": "Social events, important meetings, sexual activity (if trying to conceive)",
        },
        "luteal": {
            "name": "Luteal Phase",
            "days": "Post-ovulation to next period",
            "description": "Progesterone rises then falls. Energy decreases. Focus on maintenance, not starting new things.",
            "energy": "🌘 Declining - Wind down",
            "exercise": "Moderate exercise, swimming, walking, gentle yoga",
            "lifestyle": "Finish projects, self-care, warm environments, comfort foods",
        },
    }

    def __init__(self, goals: Optional[dict] = None, diet_prefs: Optional[dict] = None):
        self.goals = goals or {
            "trying_to_conceive": False,
            "avoiding_pregnancy": False,
            "general_wellness": True,
        }
        self.diet_prefs = diet_prefs or {
            "vegetarian": False,
            "vegan": False,
            "gluten_free": False,
            "dairy_free": False,
            "low_glycemic": True,
        }

    def get_phase_recommendations(self, cycle_phase: str) -> dict:
        """Get comprehensive recommendations for a cycle phase."""
        phase_foods = self.FOODS.get(cycle_phase, self.FOODS["follicular"])

        # Get supplements for this phase
        phase_supplements = []
        for key, supplement in self.SUPPLEMENTS.items():
            phase_info = supplement["cycle_phase"].get(cycle_phase, {})
            if phase_info.get("priority") in ["high", "medium"]:
                phase_supplements.append({
                    "key": key,
                    "name": supplement["name"],
                    "dosage": supplement["dosage"],
                    "priority": phase_info.get("priority", "low"),
                    "reason": phase_info.get("reason", ""),
                    "cautions": supplement.get("cautions", ""),
                })

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        phase_supplements.sort(key=lambda x: priority_order.get(x["priority"], 3))

        # Filter foods based on diet preferences
        recommended_foods = self._filter_foods(phase_foods["recommended"])

        return {
            "phase": cycle_phase,
            "phase_info": self.PHASE_DESCRIPTIONS.get(cycle_phase, {}),
            "focus": phase_foods["focus"],
            "key_nutrients": phase_foods["key_nutrients"],
            "recommended_foods": recommended_foods,
            "foods_to_avoid": self._filter_foods(phase_foods["foods_to_avoid"]),
            "supplements": phase_supplements,
        }

    def get_fertility_plan(self) -> dict:
        """Get a comprehensive plan for trying to conceive."""
        if not self.goals.get("trying_to_conceive"):
            return self.get_wellness_plan()

        plan = {
            "goal": "Trying to Conceive",
            "title": "Fertility Support Plan",
            "daily_foundation": self._get_daily_foundation_for_pregnancy(),
            "cycle_specific": {},
            "timing_guide": self._get_timing_guide(),
            "lifestyle": self._get_fertility_lifestyle(),
        }

        for phase in ["menstrual", "follicular", "ovulation", "luteal"]:
            plan["cycle_specific"][phase] = self.get_phase_recommendations(phase)

        return plan

    def get_avoidance_plan(self) -> dict:
        """Get guidance for avoiding pregnancy (natural family planning)."""
        if not self.goals.get("avoiding_pregnancy"):
            return self.get_wellness_plan()

        return {
            "goal": "Avoiding Pregnancy",
            "title": "Natural Family Planning Guide",
            "fertile_window_warning": "The fertile window is approximately 5 days before ovulation through 1 day after. Peak fertility is the 2-3 days before ovulation.",
            "recommendations": {
                "track_cycle": "Track your cycle meticulously. Use basal body temperature and cervical mucus for confirmation.",
                "fertile_days": "During your fertile window, use barrier methods or abstain.",
                "reliability": "Note: Calendar method alone has ~24% typical use failure rate. Combine with other methods for better protection.",
                "emergency": "Have emergency contraception plan ready.",
            },
            "cycle_fertility_map": self._get_cycle_fertility_map(),
        }

    def get_wellness_plan(self) -> dict:
        """Get general wellness plan."""
        return {
            "goal": "General Wellness",
            "title": "Cycle-Aligned Wellness Plan",
            "daily_foundation": self.get_daily_foundation(),
            "cycle_specific": {
                phase: self.get_phase_recommendations(phase)
                for phase in ["menstrual", "follicular", "ovulation", "luteal"]
            },
        }

    def get_supplement_for_symptom(self, symptom: str) -> list:
        """Recommend supplements for specific symptoms."""
        symptom_map = {
            "cramps": ["magnesium", "omega3", "curcumin"],
            "fatigue": ["iron", "b_complex", "ubiquinol", "creatine"],
            "mood_swings": ["magnesium", "b_complex", "omega3", "lithium_orotate"],
            "bloating": ["magnesium", "prebiotics", "vitamin_b6", "reduce_salt"],
            "acne": ["zinc", "vitamin_a", "omega3", "prebiotics"],
            "poor_sleep": ["magnesium", "b_complex", "vitamin_d"],
            "low_libido": ["zinc", "omega3", "vitamin_d"],
            "heavy_period": ["iron", "vitamin_c", "vitamin_b_complex"],
            "pms": ["magnesium", "vitamin_b6", "zinc", "omega3"],
            "pcos": ["nac", "myo_inositol", "chromium", "omega3", "magnesium"],
        }

        recommendations = []
        for key in symptom_map.get(symptom.lower(), []):
            if key in self.SUPPLEMENTS:
                sup = self.SUPPLEMENTS[key]
                recommendations.append({
                    "name": sup["name"],
                    "dosage": sup["dosage"],
                    "reason": f"Helps with {symptom}",
                })

        return recommendations

    def get_daily_foundation(self) -> list:
        """Get daily foundational supplements (Tier 1)."""
        foundation = []
        for key in ["omega3", "vitamin_d3k2", "magnesium", "b_complex"]:
            if key in self.SUPPLEMENTS:
                sup = self.SUPPLEMENTS[key]
                foundation.append({
                    "name": sup["name"],
                    "dosage": sup["dosage"],
                    "forms": sup["forms"] if isinstance(sup["forms"], list) else "See forms above",
                    "reason": "Foundation supplement for hormonal health",
                })
        return foundation

    def _get_daily_foundation_for_pregnancy(self) -> list:
        """Get enhanced daily foundation for pregnancy preparation."""
        foundation = self._get_daily_foundation()
        # Add pregnancy-specific
        foundation.extend([
            {
                "name": "Ubiquinol (CoQ10)",
                "dosage": "200-600mg daily",
                "reason": "Critical for egg quality, especially important before conception",
            },
            {
                "name": "Iodine",
                "dosage": "150mcg daily",
                "reason": "Essential for thyroid function and fetal brain development",
            },
        ])
        return foundation

    def _get_timing_guide(self) -> dict:
        """Get timing guide for intercourse when trying to conceive."""
        return {
            "optimal_timing": "Have intercourse every 1-2 days during fertile window",
            "fertile_window": "5 days before ovulation through 1 day after",
            "peak_days": "Days 2-3 before ovulation are most fertile",
            "sperm_survival": "Sperm can live 3-5 days in cervical mucus",
            "egg_survival": "Egg lives 12-24 hours after ovulation",
            "recommendation": "Start trying 5 days before predicted ovulation, every other day until 1 day after",
        }

    def _get_fertility_lifestyle(self) -> dict:
        """Get lifestyle recommendations for fertility."""
        return {
            "exercise": {
                "recommendation": "Moderate exercise. Avoid excessive intense training.",
                "ideal": "30-45 minutes moderate activity most days",
                "avoid": "Excessive high-intensity training (may disrupt ovulation)",
            },
            "stress": {
                "recommendation": "Stress management is critical for fertility.",
                "techniques": ["Meditation", "Yoga", "Walking in nature", "Deep breathing", "Acupuncture"],
            },
            "sleep": {
                "recommendation": "7-9 hours of quality sleep. Sleep before midnight is especially important.",
                "tips": ["Consistent sleep schedule", "Dark, cool room", "No screens 1 hour before bed"],
            },
            "environmental": {
                "avoid": ["BPA plastics", "parabens in cosmetics", "pesticides", "heavy metals"],
                "recommendation": "Use glass containers, organic when possible, natural personal care",
            },
        }

    def _get_cycle_fertility_map(self) -> dict:
        """Show which days of cycle are fertile (for avoiding pregnancy)."""
        return {
            "days": {
                "days_1_5": {"fertility": "low", "note": "Menstrual - very low fertility, but not impossible with short cycles"},
                "days_6_9": {"fertility": "very_low", "note": "Early follicular - very low fertility"},
                "days_10_14": {"fertility": "rising", "note": "Late follicular - fertility increasing"},
                "days_14_16": {"fertility": "high", "note": "Ovulation window - HIGH FERTILITY"},
                "days_17_21": {"fertility": "declining", "note": "Early luteal - fertility declining"},
                "days_22_28": {"fertility": "none", "note": "Mid-late luteal - no fertility"},
            },
            "warning": "These are based on a 28-day cycle. Individual cycles vary significantly.",
        }

    def _filter_foods(self, foods: list) -> list:
        """Filter foods based on diet preferences."""
        if not foods:
            return foods

        filtered = []
        for food in foods:
            food_lower = food.lower()

            # Remove meat for vegetarians/vegans
            if self.diet_prefs.get("vegan") and any(meat in food_lower for meat in
                                                     ["meat", "beef", "chicken", "turkey", "pork", "lamb",
                                                      "salmon", "fish", "sardines", "bone broth", "eggs"]):
                continue
            if self.diet_prefs.get("vegetarian") and any(meat in food_lower for meat in
                                                          ["meat", "beef", "chicken", "turkey", "pork", "lamb",
                                                           "salmon", "fish", "sardines", "bone broth"]):
                continue

            # Gluten-free
            if self.diet_prefs.get("gluten_free") and any(gf in food_lower for gf in
                                                           ["wheat", "barley", "rye", "pasta", "bread"]):
                continue

            # Dairy-free
            if self.diet_prefs.get("dairy_free") and any(dairy in food_lower for dairy in
                                                          ["milk", "cheese", "yogurt", "butter", "cream"]):
                continue

            filtered.append(food)

        return filtered if filtered else foods
