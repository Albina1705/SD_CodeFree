decode_record(packet)

{
    "date":"2026-07-14",
    "time":"07:42",
    "glucose":125,
    "meal":"Before meal"
}


class Reading:

    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.glucose = 0
        self.meal = ""