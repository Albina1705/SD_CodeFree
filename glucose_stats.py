from statistics import mean


def filter_readings(readings, year=None, month=None):
    result = []

    for r in readings:

        if year is not None and r.year != year:
            continue

        if month is not None and r.month != month:
            continue

        result.append(r)

    return result


def glucose_statistics(readings):

    if not readings:
        return None

    min_reading = min(readings, key=lambda r: r.glucose)
    max_reading = max(readings, key=lambda r: r.glucose)

    before = sum(1 for r in readings if r.meal == "Before meal")
    after = sum(1 for r in readings if r.meal == "After meal")
    normal = sum(1 for r in readings if r.meal == "Normal")
    control = sum(1 for r in readings if r.meal == "Control solution")

    return {
        "count": len(readings),
        "min": min_reading.glucose,
        "max": max_reading.glucose,
        "avg": round(mean(r.glucose for r in readings), 1),
        "before": before,
        "after": after,
        "normal": normal,
        "control": control,
        "min_reading": min_reading,
        "max_reading": max_reading,
    }