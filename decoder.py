DEBUG = False


class Reading:

    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.glucose = 0
        self.meal = ""

    def __str__(self):
        s = (
            f"{self.day:02d}.{self.month:02d}.{self.year} "
            f"{self.hour:02d}:{self.minute:02d} "
            f"{self.glucose} mg/dL"
        )

        if self.meal:
            s += f" [{self.meal}]"

        return s

    def to_dict(self):
        return {
            "date": f"{self.year:04d}-{self.month:02d}-{self.day:02d}",
            "time": f"{self.hour:02d}:{self.minute:02d}",
            "glucose": self.glucose,
            "meal": self.meal
        }


# ←←← ATENȚIE: funcția este în afara clasei

def decode_record(packet):
    reading = Reading()

    data = packet[4:19]

    reading.year = 2000 + data[1]
    reading.month = data[2]
    reading.day = data[3]
    reading.hour = data[4]
    reading.minute = data[5]
    reading.glucose = data[7]

    # Meal marker
    meal_flags = {
        0x00: "Normal",
        0x10: "Before meal",
        0x20: "After meal",
        0x30: "Control solution",
    }

    reading.meal = meal_flags.get(data[8] & 0x30, "")

    if DEBUG:
        print(
            f"[12]={packet[12]:02X} "
            f"[13]={packet[13]:02X} "
            f"[14]={packet[14]:02X} "
            f"[15]={packet[15]:02X} "
            f"[16]={packet[16]:02X} "
            f"[17]={packet[17]:02X} "
            f"[18]={packet[18]:02X}"
        )

    return reading