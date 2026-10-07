from flask import Flask, render_template, request
import os
import pickle

app = Flask(__name__)

MODEL_PATH = os.path.join("model", "model.pkl")
model = None

# Load your trained ML model if model/model.pkl exists.
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        print("Model load error:", e)


@app.route("/")
def home():
    return render_template("index.html", prediction=None)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        area = float(request.form["area"])
        bedrooms = float(request.form["bedrooms"])
        bathrooms = float(request.form["bathrooms"])
        stories = float(request.form["stories"])
        parking = float(request.form["parking"])
        location = request.form["location"]
        property_type = request.form["property_type"]

        # If your trained pipeline accepts all these fields, use this section.
        if model is not None:
            # Most sklearn pipelines work better with a DataFrame.
            import pandas as pd

            input_data = pd.DataFrame([{
                "area": area,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "stories": stories,
                "parking": parking,
                "location": location,
                "property_type": property_type
            }])

            predicted = float(model.predict(input_data)[0])
        else:
            # Demo fallback so the website runs even before model.pkl is added.
            location_factor = {
                "Delhi": 1.20,
                "Noida": 1.05,
                "Ghaziabad": 0.85,
                "Lucknow": 0.65,
                "Kanpur": 0.55,
                "Other": 0.50
            }.get(location, 0.50)

            property_factor = {
                "Apartment": 1.00,
                "Independent House": 1.15,
                "Villa": 1.35,
                "Builder Floor": 0.90
            }.get(property_type, 1.00)

            predicted = (
                area * 3500
                + bedrooms * 150000
                + bathrooms * 100000
                + stories * 75000
                + parking * 100000
            ) * location_factor * property_factor

        predicted = max(0, predicted)
        confidence = min(95, max(72, 78 + int(min(area / 1000, 10))))

        return render_template(
            "index.html",
            prediction=predicted,
            confidence=confidence,
            submitted=request.form
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Please enter valid house details. Error: {e}",
            submitted=request.form
        )


if __name__ == "__main__":
    app.run(debug=True)
