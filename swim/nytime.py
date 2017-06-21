"""Correctly handle date time for America/New_York.
"""

import datetime
import pytz


def get_current_date():
    """Return current time in America/New_York.
    """
    u = datetime.datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc)
    current_time = u.astimezone(pytz.timezone("America/New_York")).date()
    return current_time
