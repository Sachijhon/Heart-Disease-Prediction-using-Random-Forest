# Heart Disease Prediction Using Random Forest

A machine-learning project that explores heart disease classification using clinical attributes and a Random Forest model, with a Flask interface for collecting inputs and presenting predictions.

> **Important:** This project is for educational purposes only. It is not a medical device or a substitute for diagnosis, treatment, or advice from a qualified healthcare professional. Model outputs should not be used to make medical decisions.

## Overview

This project demonstrates an end-to-end machine-learning workflow: clinical dataset preparation, exploratory analysis, model training and evaluation, and integration of a trained model into a web application.

## Highlights

- Random Forest classification for heart disease prediction
- Jupyter Notebook for analysis and experimentation
- Flask-based application interface
- Probability-based outputs and PDF reporting
- Project documentation and academic report

## Technology Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Data processing | pandas, NumPy |
| Machine learning | scikit-learn |
| Web app | Flask, HTML, CSS |
| Model persistence | joblib |
| Reporting | ReportLab |
| Development | Jupyter Notebook, VS Code |

## Repository Contents

- `Heart_Disease_Prediction (1).ipynb` — model exploration notebook
- `App.py` — Flask application
- `heart_cleveland_upload.csv` — dataset used for the project
- `rf_heart_model.pkl` — serialized trained model
- `templates/` and `static/` — application interface assets
- `PROJECT REPORT.docx`, `synopsis.docx`, and `Heart_Disease_Report.pdf` — project documents

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sachijhon/Heart-Disease-Prediction-using-Random-Forest.git
cd Heart-Disease-Prediction-using-Random-Forest
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask pandas numpy scikit-learn joblib reportlab matplotlib jupyter
```

### 4. Run the application

Check that the expected model file and HTML templates are in the locations referenced by `App.py`. Then run:

```bash
python App.py
```

Open the local URL shown in the terminal. The exact startup requirements depend on the implementation and local configuration.

## Model Evaluation

Please see the notebook and evaluation material for the metrics produced by the actual experiment. Performance depends on the dataset, train/test split, and model configuration. Avoid interpreting a single test split as proof of clinical reliability.

## Security and Responsible Use

- Never commit real passwords, API keys, session secrets, or private data.
- Store local credentials and secrets in environment variables or ignored configuration files.
- Do not deploy Flask's development server or debug mode to production.
- Pickled/joblib model files should only be loaded from trusted sources.
- Validate inputs and configure authentication and session security before exposing the app publicly.

## Limitations and Future Work

- The dataset is limited and may not represent diverse real-world populations.
- Further validation on independent data is needed before any clinical interpretation.
- Potential improvements include reproducible training scripts, automated tests, input validation, secure configuration, model calibration analysis, and a documented deployment workflow.

## Authors

- Sachin B A
- Rohith S

Bachelor of Computer Applications project, 2025–2026.

## License

No license is currently specified. Add an appropriate license before inviting reuse or redistribution.