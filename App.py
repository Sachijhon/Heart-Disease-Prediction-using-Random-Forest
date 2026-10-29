from flask import Flask, render_template, request, send_file, redirect, url_for, session
import pandas as pd
import joblib
import json
import os
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cardio_ai_secret_key"  # REQUIRED for session

# Load trained model
saved_data = joblib.load('rf_heart_model.pkl')
MODEL = saved_data['model']
FEATURE_NAMES = saved_data['feature_names']

# Store latest report data
latest_report = {}

# Credentials file
CREDENTIAL_FILE = "credentials.json"

if not os.path.exists(CREDENTIAL_FILE):
    with open(CREDENTIAL_FILE, "w") as f:
        json.dump({
            "email": "doctor@cardioai.com",
            "password": "Cardio@123"
        }, f)

SECRET_CODE = "CARDIO2025"


# ---------------- LOGIN PAGE ---------------- #

@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    with open(CREDENTIAL_FILE, "r") as f:
        creds = json.load(f)

    if email == creds["email"] and password == creds["password"]:
        session['user'] = email
        return redirect(url_for('home'))

    return render_template('login.html', error="Invalid Email or Password")


# ---------------- FORGOT PASSWORD ---------------- #

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/verify-secret', methods=['POST'])
def verify_secret():
    email = request.form['email']
    secret_code = request.form['secret_code']

    with open(CREDENTIAL_FILE, "r") as f:
        creds = json.load(f)

    if email == creds["email"] and secret_code == SECRET_CODE:
        return render_template('forgot_password.html', verified=True, email=email)

    return render_template('forgot_password.html', error="Invalid Email or Secret Code")


@app.route('/update-password', methods=['POST'])
def update_password():
    email = request.form['email']
    new_password = request.form['new_password']

    with open(CREDENTIAL_FILE, "r") as f:
        creds = json.load(f)

    if email == creds["email"]:
        creds["password"] = new_password

        with open(CREDENTIAL_FILE, "w") as f:
            json.dump(creds, f)

        return render_template('login.html', error="Password updated successfully. Please login.")

    return redirect(url_for('forgot_password'))


# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    return render_template('index.html')


# ---------------- PREDICTION ---------------- #

@app.route('/predict', methods=['POST'])
def predict():

    if 'user' not in session:
        return redirect(url_for('login_page'))

    age = int(request.form['age'])
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    cp = int(request.form['cp'])
    trestbps = int(request.form['trestbps'])
    chol = int(request.form['chol'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    thalach = int(request.form['thalach'])
    exang = int(request.form['exang'])
    oldpeak = float(request.form['oldpeak'])
    slope = int(request.form['slope'])
    ca = int(request.form['ca'])
    thal = int(request.form['thal'])

    values = [[
        age, sex, cp, trestbps, chol,
        fbs, restecg, thalach, exang,
        oldpeak, slope, ca, thal
    ]]

    input_df = pd.DataFrame(values, columns=FEATURE_NAMES)

    proba = MODEL.predict_proba(input_df)[0]

    hd_pct = round(proba[1] * 100, 2)
    no_hd_pct = round(proba[0] * 100, 2)

    if hd_pct >= 65:
        risk = "HIGH RISK"
        advice = "Immediate cardiology consultation recommended."
    elif hd_pct >= 40:
        risk = "MODERATE RISK"
        advice = "Further cardiovascular evaluation advised."
    else:
        risk = "LOW RISK"
        advice = "Routine monitoring recommended."

    feature_values = {
        "High Cholesterol": chol > 240,
        "High Blood Pressure": trestbps > 140,
        "Low Maximum Heart Rate": thalach < 120,
        "Exercise Induced Angina": exang == 1,
        "Abnormal ECG": restecg != 0,
        "Chest Pain Symptoms": cp > 0
    }

    factors = [k for k, v in feature_values.items() if v]

    if not factors:
        factors.append("No major risk contributors detected")

    if hd_pct >= 65:
        ai_summary = "AI analysis indicates significantly elevated cardiovascular risk."
    elif hd_pct >= 40:
        ai_summary = "AI analysis suggests moderate cardiovascular risk."
    else:
        ai_summary = "AI analysis indicates low cardiovascular risk."

    global latest_report

    latest_report = {
        "prediction": hd_pct,
        "no_prediction": no_hd_pct,
        "risk": risk,
        "advice": advice,
        "factors": factors,
        "ai_summary": ai_summary,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    return render_template(
        'result.html',
        prediction=hd_pct,
        no_prediction=no_hd_pct,
        risk=risk,
        advice=advice,
        factors=factors,
        ai_summary=ai_summary
    )


# ---------------- PDF DOWNLOAD ---------------- #

@app.route('/download_report')
def download_report():

    if 'user' not in session:
        return redirect(url_for('login_page'))

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Heart Disease Report")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(140, 800, "Heart Disease Risk Report")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 760, f"Date: {latest_report['date']}")
    pdf.drawString(50, 720, f"Heart Disease: {latest_report['prediction']}%")
    pdf.drawString(50, 690, f"No Disease: {latest_report['no_prediction']}%")
    pdf.drawString(50, 660, f"Risk Level: {latest_report['risk']}")
    pdf.drawString(50, 630, f"Advice: {latest_report['advice']}")

    pdf.drawString(50, 600, "AI Summary:")
    pdf.drawString(70, 570, latest_report['ai_summary'])

    pdf.drawString(50, 530, "Risk Factors:")

    y = 500
    for f in latest_report['factors']:
        pdf.drawString(70, y, f"- {f}")
        y -= 25

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Heart_Report.pdf",
        mimetype='application/pdf'
    )


# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    return redirect(url_for('login_page'))

# ---------------- CACHE CONTROL ---------------- #

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    app.run(debug=True)