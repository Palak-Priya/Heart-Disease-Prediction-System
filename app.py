from flask import send_file
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

# ================= LOAD MODEL =================
#model = pickle.load(open('heart_model.pkl', 'rb'))
class DummyModel:
    def predict(self, x):
        return [0]

model = DummyModel()
# ================= DATABASE INIT =================
def init_db():
    conn = sqlite3.connect('heart.db')
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        inputs TEXT,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= LOGIN =================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            return redirect(url_for('home'))
        else:
            return "Invalid Login ❌"
    return render_template('login.html')

# ================= HOME =================
@app.route('/home')
def home():
    return render_template('home.html')
# ================= TYPES PAGE =================
@app.route('/types')
def types():
    return render_template('types.html')
# ================= TYPE DETAIL PAGE =================
@app.route('/type/<name>')
def type_detail(name):

    data = {
        "cad": {
            "title": "Coronary Artery Disease",
            "img": "type1.jpg",
            "desc": "Coronary Artery Disease is the narrowing or blockage of the arteries that supply your heart with blood, oxygen and nutrients. This narrowing is caused by plaque build-up (cholesterol, fat deposits and other substances), which is also called atherosclerosis. This type of heart disease is also sometimes called ischemic heart disease.Coronary artery disease is the most common kind of heart disease, and it causes most heart attacks as well as chest pain from angina.",
            "cause": "It occurs due to high cholesterol, smoking, obesity, and lack of exercise.",
            "prevention": "Maintain a healthy diet, exercise regularly, avoid smoking, and control blood pressure."
        },

        "failure": {
            "title": "Heart Failure",
            "img": "type2.jpg",
            "desc": "Heart Failure is a chronic condition caused by the heart not functioning as it should or by a problem with its structure. Heart failure can happen if the heart is too weak or too stiff or both. This can lead to fatigue, swelling in the legs and abdomen, and shortness of breath which can be from fluid in the lungs.The two most common causes of heart failure are heart attack and high blood pressure. There is no cure for heart failure, but early diagnosis, lifestyle changes and medication can help people live an active life, stay out of the hospital and live longer.",
            "cause": "Caused by high blood pressure, diabetes, or previous heart attack.",
            "prevention": "Control BP, eat healthy, reduce salt, and follow doctor advice."
        },

        "arrhythmia": {
            "title": "Arrhythmia",
            "img": "type3.jpeg",
            "desc": "Heart rhythm disorders (arrhythmias) cause disruptions in the heart’s normal rhythm. A healthy heart should beat in a regular, normal rhythm and at a healthy rate. When a person experiences an arrhythmia, their heart may beat too slowly, too quickly or in a disorganized and irregular manner.There are many types of heart arrhythmias. Some can have symptoms such as a fluttering or racing heart feeling and some can have no signs or symptoms. Some arrhythmias can be more serious, causing shortness of breath or chest pain, and in rare circumstances can be life-threatening.",
            "cause": "It occurs due to electrical signal problems in the heart.",
            "prevention": "Avoid stress, caffeine, and maintain healthy lifestyle."
        },

        "cardio": {
            "title": "Cardiomyopathy",
            "img": "type4.jpg",
            "desc": "Cardiomyopathy is a disease of the heart muscle (myocardium) that makes it harder for the heart to pump blood to the rest of the body, often leading to heart failure, arrhythmias, or severe complications. It causes the heart muscle to become enlarged, thick, or rigid. Common symptoms include fatigue, dizziness, and shortness of breath.",
            "cause": "Can be genetic or due to infections and alcohol.",
            "prevention": "Avoid alcohol, regular checkups, and healthy diet."
        },

        "valve": {
            "title": "Heart Valve Disease",
            "img": "type5.jpg",
            "desc": "Heart valves not working properly,Heart valve disease occurs when one or more of the heart’s four valves (aortic, mitral, tricuspid, pulmonary) do not function properly, disrupting blood flow. It causes valves to leak (regurgitation) or stiffen (stenosis), forcing the heart to work harder, which may cause fatigue, shortness of breath, palpitations, and chest pain.",
            "cause": "Due to infections, aging, or congenital defects.",
            "prevention": "Maintain hygiene, treat infections early."
        },

        "congenital": {
            "title": "Congenital Heart Disease",
            "img": "type6.jpg",
            "desc": "Heart defect present from birth.(CHD, heart defects) is a range of structural problem of the heart that are present during fetal development. There are many different types of CHD including abnormalities of the valves, great vessels, heart walls or chambers. They can be caused by genetic or non-genetic factors. People living with congenital heart disease and their families need support throughout every age and stage of their life. Ongoing medical care and surgical procedures can continue into adulthood.",
            "cause": "Occurs during fetal development.",
            "prevention": "Regular prenatal care and healthy pregnancy."
        },

        "pericardial": {
            "title": "Pericardial Disease",
            "img": "type7.jpg",
            "desc": "Inflammation around heart lining,Pericardial diseases are conditions affecting the pericardium—the thin, two-layered sac surrounding the heart—often causing inflammation (pericarditis) or fluid buildup (effusion). Key types include acute, chronic, or recurrent pericarditis and tamponade. Symptoms frequently involve sharp, positional chest pain, while treatment typically involves anti-inflammatories.",
            "cause": "Caused by infections or autoimmune diseases.",
            "prevention": "Treat infections on time and regular health checkups."
        }
    }

    info = data.get(name)

    return render_template("type_detail.html", info=info)

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/prevention')
def prevention():
    return render_template('prevention.html')

# ================= PREDICTION PAGE =================
@app.route('/predict_page')
def predict_page():
    return render_template('index.html')

# ================= PREDICT FUNCTION =================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 🔥 Input
        age = float(request.form['age'])
        sex = float(request.form['sex'])
        cp = float(request.form['cp'])
        trestbps = float(request.form['trestbps'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        restecg = float(request.form['restecg'])
        thalach = float(request.form['thalach'])
        exang = float(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        ca = float(request.form['ca'])
        thal = float(request.form['thal'])

        values = [age, sex, cp, trestbps, chol, fbs, restecg,
                  thalach, exang, oldpeak, slope, ca, thal]

        prediction = model.predict([values])

        # 🔥 RESULT
        if prediction[0] == 0:
            result = "No Heart Disease ❤️ (Healthy)"
        else:
            result = "Heart Disease Detected ⚠️"

        # 🔥 FEEDBACK
        details = []

        details.append(f"Age: {age} → Risk increases with age")

        if trestbps > 120:
            details.append(f"BP: {trestbps} High → Reduce salt")
        else:
            details.append(f"BP: {trestbps} Normal")

        if chol > 200:
            details.append(f"Cholesterol: {chol} High → Avoid oily food")
        else:
            details.append(f"Cholesterol: {chol} Normal")

        if thalach < 100:
            details.append(f"Heart Rate: {thalach} Low → Exercise")
        else:
            details.append(f"Heart Rate: {thalach} Good")

        if exang == 1:
            details.append("Exercise Angina: Yes → Be careful")
        else:
            details.append("Exercise Angina: No")

        if fbs > 120:
            details.append("Sugar: High → Control diet")
        else:
            details.append("Sugar: Normal")

        details.append("Overall: Maintain healthy lifestyle")

        # 🔥 SAVE TO DATABASE
        conn = sqlite3.connect('heart.db')
        c = conn.cursor()

        c.execute("INSERT INTO history (time, inputs, result) VALUES (?, ?, ?)", (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(list(values)),
            result
        ))

        conn.commit()
        conn.close()

    except:
        result = "Error in input ❌"
        details = []

    return render_template('index.html', result=result, details=details)

# ================= HISTORY =================
@app.route('/history')
def history():
    conn = sqlite3.connect('heart.db')
    c = conn.cursor()

    c.execute("SELECT * FROM history ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    import ast
    data = []
    for r in rows:
        data.append({
            "id":r[0],
            "time": r[1],
            "inputs": ast.literal_eval(r[2]),
            "result": r[3]
        })

    return render_template("history.html", data=data)
#==================REPORT DOWNLOAD==========
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

@app.route('/download/<int:id>')
def download(id):
    conn = sqlite3.connect('heart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE id=?", (id,))
    row = c.fetchone()
    conn.close()

    import ast
    inputs = ast.literal_eval(row[2])

    filename = f"report_{id}.pdf"
    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()
    elements = []

    # 🔥 HEADER
    elements.append(Paragraph("<b><font size=20 color='darkblue'>❤️ Heartify Health Report</font></b>", styles['Title']))
    elements.append(Spacer(1, 15))

    # 🔥 DATE
    elements.append(Paragraph(f"<b>Date & Time:</b> {row[1]}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # 🔥 RESULT (Color)
    if "No Heart" in row[3]:
        result_color = colors.green
    else:
        result_color = colors.red

    elements.append(Paragraph(
        f"<b>Result:</b> <font color='{ 'green' if result_color==colors.green else 'red' }'>{row[3]}</font>",
        styles['Normal']
    ))

    elements.append(Spacer(1, 20))

    # 🔥 INPUT TABLE
    labels = [
        "Age", "Sex", "Chest Pain", "BP", "Cholesterol", "Sugar",
        "ECG", "Heart Rate", "Exercise Angina", "Oldpeak",
        "Slope", "CA", "Thal"
    ]

    table_data = [["Parameter", "Value"]]

    for i in range(len(inputs)):
        table_data.append([labels[i], str(inputs[i])])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('BACKGROUND', (0,1), (-1,-1), colors.lightgrey),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    # 🔥 FOOTER
    elements.append(Paragraph("<i>Generated by Heartify AI System ❤️</i>", styles['Normal']))

    # BUILD
    doc.build(elements)

    return send_file(filename, as_attachment=True)

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)