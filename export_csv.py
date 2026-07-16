import csv

def save_csv(readings, filename="readings.csv"):

    with open(filename, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f, delimiter=";")

        writer.writerow(["Date", "Time", "Glucose (mg/dL)", "Meal"])

        for r in readings:
            writer.writerow([
                f"{r.year:04d}-{r.month:02d}-{r.day:02d}",
                f"{r.hour:02d}:{r.minute:02d}",
                r.glucose,
                r.meal
            ])

    