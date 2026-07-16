import json

from protocol import SDCodefreeProtocol
from decoder import decode_record
from export_csv import save_csv

meter = SDCodefreeProtocol(debug=True)

try:
    print("Conectare...")
    meter.connect()
    print("OK!")

    readings = meter.download_all()

    print("Număr:", len(readings))

    for r in readings:
     print(r.to_dict())

    import os

    print("Scriu în:", os.path.abspath("output/readings.json"))

    data = [r.to_dict() for r in readings]
    print("Data =", data)
    with open("output/readings.json", "w", encoding="utf-8") as f:
        json.dump(
            [r.to_dict() for r in readings],
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Fișier readings.json salvat.")

    save_csv(readings, "output/readings.csv")

    print("Fișier output/readings.csv salvat.")
    print("Număr înregistrări:", len(readings))

finally:
    meter.disconnect()
    print("Port închis.")