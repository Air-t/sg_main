from datetime import datetime, timedelta


def now_plus_15_min():
    """Return actual datetime plus 15min ahead"""
    return datetime.now() + timedelta(minutes=15)


def get_mins(start, end):
    try:
        mins = int((end - start).total_seconds() / 60.0)
        return mins
    except TypeError:
        print("Time not converted.")
        return None
