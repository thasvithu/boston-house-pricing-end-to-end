import pickle
from flask import Flask, request, jsonify, render_template, url_for, flash
import numpy as np

app = Flask(__name__)
app.secret_key = "change-this-secret"  # TODO: use env var in production

# Load the model artifacts
with open("regression.pkl", "rb") as f:
    regmodel = pickle.load(f)
with open("scaling.pkl", "rb") as f:
    scaler = pickle.load(f)

# Define the expected feature order for both API and form inputs
FEATURES = [
    "CRIM",
    "ZN",
    "INDUS",
    "CHAS",
    "NOX",
    "RM",
    "AGE",
    "DIS",
    "RAD",
    "TAX",
    "PTRATIO",
    "B",
    "LSTAT",
]


@app.route("/")
def home():
    return render_template("home.html", prediction=None, form_values={})


@app.route("/predict_api", methods=["POST"])
def predict_api():
    payload = request.get_json(silent=True) or {}
    if "data" not in payload or not isinstance(payload["data"], dict):
        return jsonify({"error": "Expected JSON with 'data' object of feature values."}), 400

    data = payload["data"]
    try:
        # Extract values in the fixed order
        values = [float(data[f]) for f in FEATURES]
    except KeyError as e:
        return jsonify({"error": f"Missing feature: {str(e)}"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "All feature values must be numeric."}), 400

    X = np.array(values, dtype=float).reshape(1, -1)
    X_scaled = scaler.transform(X)
    y_pred = regmodel.predict(X_scaled)
    return jsonify({"prediction": float(y_pred[0])})


@app.route("/predict", methods=["POST"])
def predict():
    form = request.form
    try:
        values = []
        for f in FEATURES:
            val = form.get(f, "").strip()
            if val == "":
                raise ValueError(f"Missing value for {f}")
            values.append(float(val))
    except ValueError as e:
        flash(str(e), "error")
        return render_template("home.html", form_values=form, prediction=None)

    X = np.array(values, dtype=float).reshape(1, -1)
    X_scaled = scaler.transform(X)
    y_pred = regmodel.predict(X_scaled)

    return render_template(
        "home.html",
        prediction=float(y_pred[0]),
        form_values=form,
    )


if __name__ == "__main__":
    app.run(debug=True)
