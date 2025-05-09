from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Weekly meal plan template
weekly_meal_templates = {
    "Vata": {
        "breakfast": ["Warm oatmeal with almonds", "Fruit smoothie", "Steamed idli", "Herbal tea", "Upma", "Chia pudding", "Ragi porridge"],
        "lunch": ["Quinoa with vegetables", "Moong dal khichdi", "Steamed rice with veggies", "Tofu curry", "Chapati with dal", "Vegetable pulao", "Lentil soup"],
        "dinner": ["Pumpkin soup", "Light dal with rice", "Stuffed paratha", "Vegetable stew", "Clear soup", "Cabbage rolls", "Millet khichdi"]
    },
    "Pitta": {
        "breakfast": ["Coconut water", "Fruit bowl", "Rice flakes with banana", "Mint tea", "Sattu drink", "Sabudana khichdi", "Watermelon juice"],
        "lunch": ["Brown rice and moong dal", "Bottle gourd curry", "Amla rice", "Barley khichdi", "Cucumber salad", "Sweet potato curry", "Beetroot sabzi"],
        "dinner": ["Lauki soup", "Steamed vegetables", "Vegetable soup", "Curd rice", "Mung dal chilla", "Kadhi with rice", "Herbal tea with rice flakes"]
    },
    "Kapha": {
        "breakfast": ["Besan chilla", "Vegetable poha", "Herbal tea", "Nut milk smoothie", "Ragi dosa", "Sprouts salad", "Protein porridge"],
        "lunch": ["Tofu rice bowl", "Chapati with paneer sabzi", "Sweet potato curry", "Moong sprouts salad", "Chickpea salad", "Quinoa pulao", "Brown rice and lentils"],
        "dinner": ["Khichdi with ghee", "Steamed greens", "Lentil soup", "Broccoli stir fry", "Zucchini curry", "Stuffed paratha", "Bottle gourd stew"]
    }
}

@app.route('/custom_diet_plan', methods=['POST'])
def generate_custom_diet_plan():
    data = request.get_json()

    dosha = data.get('dosha')
    goal = data.get('goal')
    duration = data.get('duration')
    diseases = data.get('diseases', [])

    if not dosha or dosha not in weekly_meal_templates:
        return jsonify({'error': 'Invalid or missing dosha type'}), 400

    # Generate 7-day diet plan
    meal_template = weekly_meal_templates[dosha]
    week_plan = []
    for day in range(7):
        day_plan = {
            "day": f"Day {day + 1}",
            "breakfast": meal_template["breakfast"][day % len(meal_template["breakfast"])],
            "lunch": meal_template["lunch"][day % len(meal_template["lunch"])],
            "dinner": meal_template["dinner"][day % len(meal_template["dinner"])]
        }
        week_plan.append(day_plan)

    # Generate recommendations
    recommendations = []
    if goal:
        goal = goal.lower()
        if "weight loss" in goal:
            recommendations.append("Focus on lighter dinners and avoid sugar-rich foods.")
        elif "muscle gain" in goal:
            recommendations.append("Include more protein-rich legumes and paneer.")
        elif "detox" in goal:
            recommendations.append("Drink warm water with lemon every morning and eat steamed vegetables.")

    if duration:
        try:
            weeks = int(duration.split()[0])
            if weeks < 2:
                recommendations.append("Follow the plan for at least 2 weeks for visible results.")
            elif weeks >= 4:
                recommendations.append("You're on track for long-term benefits. Stay consistent!")
        except:
            recommendations.append("Duration format not recognized. Use 'x weeks' format.")

    for d in diseases:
        d = d.lower()
        if "diabetes" in d:
            recommendations.append("Avoid sugary fruits; include bitter gourd and fenugreek.")
        if "hypertension" in d or "bp" in d:
            recommendations.append("Reduce salt and processed foods; prefer steamed dishes.")
        if "thyroid" in d:
            recommendations.append("Limit cabbage/cauliflower; add iodine-rich foods.")

    return jsonify({
        "dosha": dosha,
        "goal": goal,
        "duration": duration,
        "diseases": diseases,
        "weekly_meal_plan": week_plan,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
