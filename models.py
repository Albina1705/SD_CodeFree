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
