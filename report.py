import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# 1. DEFINIREA FUNCȚIEI PENTRU RAPORT PDF
def generate_pdf(data, statistics, chart_path, pdf_path):
    # Crează folderul de output dacă nu există
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Configurare document PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Titlu Raport
    story.append(Paragraph("<b>Raport Medical: Evolutie Glicemie</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    # Adăugare Statistici în text
    text_statistici = f"""
    <b>Statistici Generale:</b><br/>
    • Valoare Medie: {statistics['medie']:.2f} mg/dL<br/>
    • Valoare Maxima: {statistics['maxima']} mg/dL<br/>
    • Valoare Minima: {statistics['minima']} mg/dL<br/>
    • Total Masuratori: {statistics['total']}
    """
    story.append(Paragraph(text_statistici, styles["BodyText"]))
    story.append(Spacer(1, 25))

    # Adăugare Grafic (Verificăm dacă imaginea generată de chart.py există)
    if os.path.exists(chart_path):
        story.append(Paragraph("<b>Grafic Evolutiv:</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))
        # Ajustează dimensiunea imaginii în PDF (lățime, înălțime)
        story.append(Image(chart_path, width=400, height=200))
    else:
        story.append(Paragraph("<font color='red'><i>Graficul glucose_chart.png nu a fost gasit. Ruleaza mai intai chart.py!</i></font>", styles["BodyText"]))

    # Construire PDF
    doc.build(story)
    print(f" Raportul PDF a fost salvat cu succes în: {pdf_path}")


# 2. PREGĂTIREA DATELOR ȘI STATISTICILOR (Rezolvă "filtered" și "stats")
try:
    # Încărcăm aceleași date din export.csv
    df = pd.read_csv("export.csv")
    filtered = df.tail(30)  # Păstrăm aceleași date filtrate

    # Identificăm coloana cu valorile glicemiei (presupunem că e a doua coloană)
    col_valoare = df.columns[1]

    # Calculăm statisticile cerute de funcție
    stats = {
        "medie": filtered[col_valoare].mean(),
        "maxima": filtered[col_valoare].max(),
        "minima": filtered[col_valoare].min(),
        "total": len(filtered)
    }

    # 3. APELUL CORECT AL FUNCȚIEI (Codul tău original)
    generate_pdf(
        filtered,
        stats,
        "output/glucose_chart.png",
        "output/report.pdf"
    )

except FileNotFoundError:
    print(" Eroare: Nu s-a putut genera PDF-ul deoarece 'export.csv' lipsește.")
except Exception as e:
    print(f" A apărut o eroare la procesarea raportului: {e}")
