# filter.py

def filter_readings(
    readings,
      year=None,
      month=None,
      day=None,
      meal=None,
      min_glucose=None,
      max_glucose=None
    ):
    """
    Filtrează lista de Reading.

    Exemple:
        filter_readings(readings, year=2026)
        filter_readings(readings, year=2026, month=7)
        filter_readings(readings, year=2026, month=7, day=19)
    """

    result = []

    for r in readings:

        if year is not None and r.year != year:
            continue

        if month is not None and r.month != month:
            continue

        if day is not None and r.day != day:
            continue

        result.append(r)

    return result