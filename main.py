import json

from protocol import SDCodefreeProtocol
from export_csv import save_csv
from filter import filter_readings



meter = SDCodefreeProtocol(port=None, debug=True, analyze_protocol=True)

try:
    print("Conectare...")
    meter.connect()
    print("OK!")

    readings = meter.download_all()

    readings_2026_07 = filter_readings(
        readings,
        year=2026,
        month=7
    )

    print()
    print(f"Total măsurători : {len(readings)}")
    print(f"Iulie 2026       : {len(readings_2026_07)}")

    print("Număr:", len(readings))

    for r in readings_2026_07:
     print(r)

    for r in readings:
     print(r.to_dict())

    import os


    data = [r.to_dict() for r in readings]

    print("Scriu în:", os.path.abspath("output/readings.json"))

    with open("output/readings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Fișier readings.json salvat.")

    save_csv(readings, "output/readings.csv")
    save_csv(
        readings_2026_07,
        "output/readings_2026_07.csv"
    )

    print("Număr înregistrări:", len(readings))
    

finally:
    meter.disconnect()
    print("Port închis.")