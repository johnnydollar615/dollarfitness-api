
from flask import Flask, request, jsonify

app = Flask(__name__)

# Core logic
def calculate_macros(age, weight_lbs, height_inches, goal, training_days, activity_level):
    weight_kg = weight_lbs * 0.4536
    height_cm = height_inches * 2.54
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }
    activity_factor = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * activity_factor

    if goal == "bulk":
        calories = tdee + 300
    elif goal == "cut":
        calories = tdee - 300
    else:
        calories = tdee

    protein_grams = weight_lbs * 1
    fat_grams = weight_lbs * 0.4
    protein_cals = protein_grams * 4
    fat_cals = fat_grams * 9
    carb_cals = calories - (protein_cals + fat_cals)
    carbs_grams = carb_cals / 4

    return {
        "calories": round(calories),
        "protein_grams": round(protein_grams),
        "carbs_grams": round(carbs_grams),
        "fats_grams": round(fat_grams)
    }

def generate_workout_split(training_days):
    splits = {
        3: ["Push", "Pull", "Legs", "Rest", "Rest", "Rest", "Rest"],
        4: ["Upper", "Lower", "Push", "Pull", "Rest", "Rest", "Rest"],
        5: ["Push", "Pull", "Legs", "Upper", "Lower", "Rest", "Rest"],
        6: ["Push", "Pull", "Legs", "Push", "Pull", "Legs", "Rest"],
        7: ["Push", "Pull", "Legs", "Upper", "Lower", "Full Body", "Mobility"]
    }
    return splits.get(training_days, splits[5])

def generate_meal_plan(goal, calories):
    if goal == "bulk":
        return {
            "breakfast": "6 eggs, 2 slices toast, banana, peanut butter",
            "lunch": "Chicken breast, rice, mixed veggies, olive oil",
            "dinner": "Ground beef, potatoes, broccoli, shredded cheese",
            "snacks": "Protein shake, oats, almonds, Greek yogurt"
        }
    elif goal == "cut":
        return {
            "breakfast": "3 eggs, spinach, black coffee",
            "lunch": "Grilled chicken salad, vinaigrette",
            "dinner": "Tilapia, steamed broccoli, sweet potato",
            "snacks": "Whey protein, cucumber slices, almonds"
        }
    else:
        return {
            "breakfast": "4 eggs, oatmeal with banana",
            "lunch": "Turkey sandwich on whole wheat, veggies",
            "dinner": "Grilled chicken, rice, broccoli",
            "snacks": "Protein shake, cottage cheese, apple"
        }

@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
    macros = calculate_macros(
        data["age"],
        data["weight_lbs"],
        data["height_inches"],
        data["goal"],
        data["training_days"],
        data["activity_level"]
    )
    workout_split = generate_workout_split(data["training_days"])
    meal_plan = generate_meal_plan(data["goal"], macros["calories"])

    return jsonify({
        **macros,
        "workout_split": workout_split,
        "meal_plan": meal_plan
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
age = data.get("age")
weight_lbs = data.get("weight_lbs")
height_inches = data.get("height_inches")
goal = data.get("goal")
training_days = data.get("training_days")
activity_level = data.get("activity_level")
macros = calculate_macros(age, weight_lbs, height_inches, goal, training_days, activity_level)
return jsonify(macros)
if __name__ == "__main__":
app.run(host="0.0.0.0", port=3000)
