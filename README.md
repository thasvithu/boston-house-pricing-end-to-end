<div align="center">

# Boston House Price Prediction

Predict median house values in Boston using a trained scikit-learn model served by a Flask web app, with a clean UI and a from-scratch EDA/training notebook.

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.x-orange)
![License](https://img.shields.io/badge/License-Open-brightgreen)

</div>

## Overview

This project predicts Boston house prices using 13 classic features from the Boston Housing dataset. It includes:

- A Flask server exposing a browser UI and a JSON API.
- A styled, responsive HTML form for quick predictions.
- A Jupyter notebook that walks through EDA, modeling, evaluation, and saving artifacts.
- Pre-trained artifacts (`regression.pkl`, `scaling.pkl`) ready to use.

## Project structure

```
.
├─ app.py                       # Flask app: UI + JSON API
├─ boston.csv                   # Dataset
├─ Boston House Price Prediction.ipynb  # From-scratch EDA + training
├─ regression.pkl               # Trained Linear Regression model
├─ scaling.pkl                  # Trained StandardScaler
├─ Templates/
│   └─ home.html               # Beautiful, responsive UI
├─ static/
│   └─ styles.css              # UI styling
├─ requirements.txt            # Runtime dependencies (pip)
├─ pyproject.toml              # Alternative dependency spec (uv/pep621)
├─ uv.lock                     # uv lockfile (optional)
├─ LICENSE                     # License file
└─ README.md                   # You are here
```

## Features

- Web UI for interactive predictions (13 inputs with helpful labels)
- JSON API endpoint for programmatic access
- Reproducible notebook with clear commentary and metrics (MAE, RMSE, R², Adjusted R²)
- Artifacts saved and wired into the app

## Quickstart (Windows PowerShell)

Prerequisites: Python 3.13 (recommended). If you hit install issues with some packages, Python 3.11 works well too.

```powershell
# Create and activate a virtual environment
py -3.13 -m venv .venv
. .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python .\app.py
```

Open http://127.0.0.1:5000/ and try a prediction in the browser.

### Using uv (optional)

If you prefer uv with `pyproject.toml`:

```powershell
# Install and run with uv
uv sync
uv run python .\app.py
```

## API usage

Endpoint: `POST /predict_api`

Request body (JSON):

```json
{
	"data": {
		"CRIM": 0.00632,
		"ZN": 18.0,
		"INDUS": 2.31,
		"CHAS": 0.0,
		"NOX": 0.538,
		"RM": 6.575,
		"AGE": 65.2,
		"DIS": 4.09,
		"RAD": 1.0,
		"TAX": 296.0,
		"PTRATIO": 15.3,
		"B": 396.9,
		"LSTAT": 4.98
	}
}
```

Response:

```json
{ "prediction": 24.12 }
```

PowerShell example:

```powershell
$body = @{ data = @{ CRIM=0.00632; ZN=18; INDUS=2.31; CHAS=0; NOX=0.538; RM=6.575; AGE=65.2; DIS=4.09; RAD=1; TAX=296; PTRATIO=15.3; B=396.9; LSTAT=4.98 } } | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/predict_api -Body $body -ContentType "application/json"
```

## Model and features

- Estimator: scikit-learn `LinearRegression` (baseline). The notebook also compares Ridge and Lasso.
- Scaling: `StandardScaler` fit on training data; applied to inputs at inference time.
- Target: `PRICE` (in $1000s).
- Feature order (must match exactly):
	- `CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT`

## Notebook workflow

Open `Boston House Price Prediction.ipynb` and run top-to-bottom:

1. Setup & imports (defines `FEATURES` contract and random seed)
2. Load & validate data (shape, schema, null checks)
3. EDA (correlations, key relationships: RM↑ → PRICE↑, LSTAT↑ → PRICE↓)
4. Split & scale (70/30 split; prevent leakage)
5. Modeling with CV (Linear baseline + Ridge/Lasso with CV)
6. Evaluation (MAE, RMSE, R², Adjusted R²; diagnostic plots)
7. Persistence (writes `scaling.pkl` and `regression.pkl`)

To refresh artifacts, re-run the notebook and re-launch the app.

## Troubleshooting

- Flask/numpy import errors: ensure your virtual environment is activated and `pip install -r requirements.txt` has completed without errors.
- Python 3.13 wheels: if you face binary install issues, try Python 3.11.
- JSON errors: the API expects a `data` object with all 13 features numeric; missing or non-numeric values return 400 with an error message.
- Wrong predictions: ensure the feature order matches the list above; the server extracts inputs in that fixed order.

## License

See `LICENSE` for details.

