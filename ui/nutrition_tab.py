"""
Nutrition Tab - Food and supplement recommendations by cycle phase.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class NutritionTab(ttk.Frame):
    """Nutrition and supplement guidance UI."""

    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data = data_manager

        # Import nutrition advisor
        from nutrition_advisor import NutritionAdvisor

        goals = self.data.get_goals()
        diet_prefs = self.data.get_diet_preferences()
        self.advisor = NutritionAdvisor(goals, diet_prefs)

        self._create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.refresh()

    def _create_widgets(self):
        """Create nutrition UI."""
        # Left panel - Phase selector and recommendations
        left_frame = ttk.LabelFrame(self, text="Cycle Phase Recommendations", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Phase selector
        phase_frame = ttk.Frame(left_frame)
        phase_frame.pack(fill=tk.X, pady=5)

        ttk.Label(phase_frame, text="Select Phase:").pack(side=tk.LEFT, padx=5)

        self.phase_var = tk.StringVar(value="menstrual")
        phase_options = ["menstrual", "follicular", "ovulation", "luteal"]
        phase_labels = {
            "menstrual": "🩸 Menstrual",
            "follicular": "🌱 Follicular",
            "ovulation": "🌟 Ovulation",
            "luteal": "🍂 Luteal",
        }

        for phase in phase_options:
            ttk.Radiobutton(phase_frame, text=phase_labels[phase],
                          variable=self.phase_var, value=phase,
                          command=self._on_phase_change).pack(side=tk.LEFT, padx=5)

        # Phase info
        self.phase_info_text = tk.Text(left_frame, height=8, font=("Arial", 10), wrap=tk.WORD)
        self.phase_info_text.pack(fill=tk.X, pady=5)
        self.phase_info_text.config(state=tk.DISABLED)

        # Food recommendations
        foods_frame = ttk.LabelFrame(left_frame, text="Food Recommendations", padding=5)
        foods_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.foods_text = tk.Text(foods_frame, height=10, font=("Arial", 9), wrap=tk.WORD)
        self.foods_text.pack(fill=tk.BOTH, expand=True)
        self.foods_text.config(state=tk.DISABLED)

        # Right panel - Supplements
        right_frame = ttk.LabelFrame(self, text="Supplement Guide", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Supplement priority
        ttk.Label(right_frame, text="High Priority:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        self.high_supplements = tk.Listbox(right_frame, font=("Arial", 9), height=6)
        self.high_supplements.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_frame, text="Medium Priority:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        self.med_supplements = tk.Listbox(right_frame, font=("Arial", 9), height=6)
        self.med_supplements.pack(fill=tk.X, pady=(0, 10))

        # Supplement detail
        self.supplement_detail = tk.Text(right_frame, height=10, font=("Arial", 9), wrap=tk.WORD)
        self.supplement_detail.pack(fill=tk.BOTH, expand=True)
        self.supplement_detail.config(state=tk.DISABLED)

        # Bottom - Symptom relief
        symptom_frame = ttk.LabelFrame(self, text="Symptom Relief", padding=10)
        symptom_frame.pack(fill=tk.X, padx=5, pady=5)

        symptom_select_frame = ttk.Frame(symptom_frame)
        symptom_select_frame.pack(fill=tk.X)

        ttk.Label(symptom_select_frame, text="I'm experiencing:").pack(side=tk.LEFT, padx=5)

        self.symptom_var = tk.StringVar(value="cramps")
        symptom_options = [
            ("cramps", "Cramps"),
            ("fatigue", "Fatigue"),
            ("mood_swings", "Mood Swings"),
            ("bloating", "Bloating"),
            ("acne", "Acne"),
            ("poor_sleep", "Poor Sleep"),
            ("pms", "PMS"),
            ("pcos", "PCOS"),
        ]

        symptom_dropdown = ttk.Combobox(symptom_select_frame, textvariable=self.symptom_var,
                                       values=[s[0] for s in symptom_options], state="readonly", width=15)
        symptom_dropdown.pack(side=tk.LEFT, padx=5)
        symptom_dropdown.bind("<<ComboboxSelected>>", self._on_symptom_change)

        ttk.Button(symptom_select_frame, text="Get Recommendations",
                  command=self._show_symptom_recs).pack(side=tk.LEFT, padx=5)

        self.symptom_text = tk.Text(symptom_frame, height=6, font=("Arial", 9), wrap=tk.WORD)
        self.symptom_text.pack(fill=tk.X, pady=5)
        self.symptom_text.config(state=tk.DISABLED)

        # Goals indicator
        goals_frame = ttk.Frame(self)
        goals_frame.pack(fill=tk.X, padx=5, pady=2)

        goals = self.data.get_goals()
        goal_text = []
        if goals.get("trying_to_conceive"):
            goal_text.append("🤰 Trying to Conceive")
        if goals.get("avoiding_pregnancy"):
            goal_text.append("🛡️ Avoiding Pregnancy")
        if goals.get("general_wellness"):
            goal_text.append("💚 General Wellness")

        if goal_text:
            ttk.Label(goals_frame, text=" | ".join(goal_text),
                     font=("Arial", 9, "bold"), foreground="#2E7D32").pack(anchor=tk.W)

    def refresh(self):
        """Refresh nutrition information."""
        self._on_phase_change()
        self._update_goals_display()

    def _on_phase_change(self):
        """Update recommendations when phase changes."""
        phase = self.phase_var.get()
        recommendations = self.advisor.get_phase_recommendations(phase)

        # Update phase info
        phase_info = recommendations.get("phase_info", {})
        info_text = (
            f"{phase_info.get('name', phase.capitalize())} {phase_info.get('days', '')}\n\n"
            f"{phase_info.get('description', '')}\n\n"
            f"{phase_info.get('energy', '')}\n"
            f"Exercise: {phase_info.get('exercise', '')}\n"
            f"Lifestyle: {phase_info.get('lifestyle', '')}"
        )

        self.phase_info_text.config(state=tk.NORMAL)
        self.phase_info_text.delete(1.0, tk.END)
        self.phase_info_text.insert(tk.END, info_text)
        self.phase_info_text.config(state=tk.DISABLED)

        # Update foods
        foods_text = (
            f"Focus: {recommendations.get('focus', '')}\n\n"
            f"Key Nutrients: {', '.join(recommendations.get('key_nutrients', []))}\n\n"
            f"✅ Recommended:\n"
        )
        for food in recommendations.get("recommended_foods", []):
            foods_text += f"  • {food}\n"

        foods_text += f"\n❌ Limit:\n"
        for food in recommendations.get("foods_to_avoid", []):
            foods_text += f"  • {food}\n"

        self.foods_text.config(state=tk.NORMAL)
        self.foods_text.delete(1.0, tk.END)
        self.foods_text.insert(tk.END, foods_text)
        self.foods_text.config(state=tk.DISABLED)

        # Update supplements
        self.high_supplements.delete(0, tk.END)
        self.med_supplements.delete(0, tk.END)

        high_supps = []
        med_supps = []

        for sup in recommendations.get("supplements", []):
            if sup["priority"] == "high":
                self.high_supplements.insert(tk.END, f"{sup['name']} - {sup['dosage']}")
            else:
                self.med_supplements.insert(tk.END, f"{sup['name']} - {sup['dosage']}")

        # Bind click events for supplement details
        self.high_supplements.bind("<<ListboxSelect>>", self._on_supplement_click)
        self.med_supplements.bind("<<ListboxSelect>>", self._on_supplement_click)

        # Show detail for first high priority supplement
        if recommendations.get("supplements"):
            first_sup = recommendations["supplements"][0]
            self._show_supplement_detail(first_sup)

    def _on_supplement_click(self, event):
        """Show supplement details on click."""
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return

        # Find the supplement
        phase = self.phase_var.get()
        recommendations = self.advisor.get_phase_recommendations(phase)

        sup_list = widget.get(0, widget.size())
        index = selection[0]

        for sup in recommendations.get("supplements", []):
            if sup["name"] in sup_list[index]:
                self._show_supplement_detail(sup)
                break

    def _show_supplement_detail(self, supplement: dict):
        """Show detailed supplement information."""
        from nutrition_advisor import NutritionAdvisor
        advisor = NutritionAdvisor(self.data.get_goals(), self.data.get_diet_preferences())

        # Look up full supplement info
        sup_key = None
        for key, sup_data in advisor.SUPPLEMENTS.items():
            if sup_data["name"] == supplement["name"]:
                sup_key = key
                break

        if not sup_key or sup_key not in advisor.SUPPLEMENTS:
            return

        sup = advisor.SUPPLEMENTS[sup_key]

        detail = (
            f"{sup['name']}\n"
            f"{'='*40}\n\n"
            f"Tier: {sup['tier']}\n"
            f"Daily Dosage: {sup['dosage']}\n"
            f"Forms: {sup['forms'] if isinstance(sup['forms'], list) else list(sup['forms'].values()) if isinstance(sup['forms'], dict) else sup['forms']}\n\n"
            f"Why now: {supplement.get('reason', '')}\n\n"
        )

        goals = self.data.get_goals()
        if goals.get("trying_to_conceive"):
            detail += f"For Pregnancy: {sup.get('for_pregnancy', 'N/A')}\n\n"
        elif goals.get("avoiding_pregnancy"):
            detail += f"Fertility Impact: {sup.get('for_avoidance', 'N/A')}\n\n"

        detail += f"⚠️ {sup.get('cautions', '')}"

        self.supplement_detail.config(state=tk.NORMAL)
        self.supplement_detail.delete(1.0, tk.END)
        self.supplement_detail.insert(tk.END, detail)
        self.supplement_detail.config(state=tk.DISABLED)

    def _on_symptom_change(self, event):
        """Update when symptom changes."""
        self._show_symptom_recs()

    def _show_symptom_recs(self):
        """Show supplement recommendations for selected symptom."""
        symptom = self.symptom_var.get()

        recommendations = self.advisor.get_supplement_for_symptom(symptom)

        if not recommendations:
            text = f"No specific supplement recommendations found for {symptom}.\n\nTry tracking your cycle phase for phase-specific guidance."
        else:
            text = f"Recommendations for {symptom.replace('_', ' ').title()}:\n\n"
            for rec in recommendations:
                text += f"• {rec['name']}\n"
                text += f"  Dosage: {rec['dosage']}\n\n"

        text += "Note: Always test with blood work when possible. Start one supplement at a time and wait 2-3 weeks before adding another."

        self.symptom_text.config(state=tk.NORMAL)
        self.symptom_text.delete(1.0, tk.END)
        self.symptom_text.insert(tk.END, text)
        self.symptom_text.config(state=tk.DISABLED)

    def _update_goals_display(self):
        """Update goals display."""
        # This is handled in the main UI now
        pass
