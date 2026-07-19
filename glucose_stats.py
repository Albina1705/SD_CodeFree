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

    values = [r.glucose for r in readings]

    before = sum(1 for r in readings if r.meal == "Before meal")
    after = sum(1 for r in readings if r.meal == "After meal")
    normal = sum(1 for r in readings if r.meal == "Normal")
    control = sum(1 for r in readings if r.meal == "Control solution")

    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": round(mean(values), 1),
        "before": before,
        "after": after,
        "normal": normal,
        "control": control,
    }