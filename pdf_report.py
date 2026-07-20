from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def export_pdf(readings, stats, filename="output/SD_CodeFree_Report_All.pdf"):

    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "SD CodeFree Glucose Report")

    y -= 30

    c.setFont("Helvetica", 11)

    c.drawString(50, y, f"Records : {stats['count']}")
    y -= 18

    c.drawString(50, y, f"Minimum : {stats['min']} mg/dL")
    y -= 18

    c.drawString(50, y, f"Maximum : {stats['max']} mg/dL")
    y -= 18

    c.drawString(50, y, f"Average : {stats['avg']:.1f} mg/dL")

    y -= 35

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Date")
    c.drawString(140, y, "Time")
    c.drawString(210, y, "Glucose")
    c.drawString(300, y, "Meal")

    y -= 18
    c.setFont("Helvetica", 10)

    for r in readings:

        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        c.drawString(50, y, f"{r.year:04d}-{r.month:02d}-{r.day:02d}")
        c.drawString(140, y, f"{r.hour:02d}:{r.minute:02d}")
        c.drawString(210, y, str(r.glucose))
        c.drawString(300, y, str(r.meal))

        y -= 15

    c.save()

    print(f"Raport PDF salvat: {filename}")