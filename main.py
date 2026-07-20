import json
import os
from protocol import SDCodefreeProtocol
from export_csv import save_csv
from emailer import send_email
from glucose_stats import filter_readings, glucose_statistics
from pdf_report import export_pdf






meter = SDCodefreeProtocol(port=None, debug=True, analyze_protocol=True)




try:
    print("Conectare...")
    meter.connect()
    print("OK!")

    readings = meter.download_all()

    year_input = input("An (Enter = toate): ").strip()
    month_input = input("Luna (Enter = toate): ").strip()

    year = int(year_input) if year_input else None
    month = int(month_input) if month_input else None

    filtered = filter_readings(readings, year, month)

    stats = glucose_statistics(filtered)


    

    DEBUG = False

    if DEBUG:

        for r in filtered:

            print(r.to_dict())

    data = [r.to_dict() for r in filtered]

    print("Scriu în:", os.path.abspath("output/readings.json"))

    import os

    OUTPUT_DIR = "output"

    json_file = os.path.join(OUTPUT_DIR, "readings.json")
    csv_file = os.path.join(OUTPUT_DIR, "readings.csv")
    pdf_file = os.path.join(OUTPUT_DIR, "SD_CodeFree_Report_All.pdf")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open("output/readings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


    print("Fișier readings.json salvat.")

    save_csv(filtered, "output/readings.csv")

    export_pdf(filtered, stats)

    # Creează automat câte un fișier CSV pentru fiecare lună
    monthly_data = {}

    for r in filtered:
        key = (r.year, r.month)
        monthly_data.setdefault(key, []).append(r)

    monthly_count = 0

    for (y, m), readings in sorted(monthly_data.items()):
        monthly_filename = f"output/readings_{y}_{m:02d}.csv"
        save_csv(readings, monthly_filename, verbose=False)
        monthly_count += 1

    print(f"Au fost generate {monthly_count} fișiere CSV lunare.")

    

        
        
        
    send_email(
        subject="Raport glicemie SD CodeFree",
        body="Atașat găsiți raportul glicemiei.",
        attachment="output/readings.csv"
)
    

   
    if not filtered:
        print("\nNu există înregistrări pentru perioada selectată.")
    else:
        if year is None and month is None:
            perioada = "Toate înregistrările"
        elif year is not None and month is None:
            perioada = f"Anul {year}"
        elif year is None and month is not None:
            perioada = f"Luna {month:02d}"
        else:
            perioada = f"{month:02d}/{year}"

    print("\n====================================")
    print(f"Perioada selectată : {perioada}")
    print(f"Înregistrări       : {len(filtered)}")
    print("====================================")

    
    print("\n===== STATISTICI =====")

    print(f"Înregistrări : {stats['count']}")

    print(
        f"Minim        : {stats['min']} mg/dL "
        f"({stats['min_reading'].day:02d}."
        f"{stats['min_reading'].month:02d}."
        f"{stats['min_reading'].year} "
        f"{stats['min_reading'].hour:02d}:"
        f"{stats['min_reading'].minute:02d})"
    )

    print(
        f"Maxim        : {stats['max']} mg/dL "
        f"({stats['max_reading'].day:02d}."
        f"{stats['max_reading'].month:02d}."
        f"{stats['max_reading'].year} "
        f"{stats['max_reading'].hour:02d}:"
        f"{stats['max_reading'].minute:02d})"
    )

    print(f"Medie        : {stats['avg']} mg/dL")

    print(
    f"Normal       : {stats['normal']}\n"
    f"Before meal  : {stats['before']}\n"
    f"After meal   : {stats['after']}\n"
    f"Control      : {stats['control']}"
)
    
    meter.disconnect()
    print("Port închis.")

except Exception as e:
    print(f"A apărut o eroare în timpul execuției: {e}")
