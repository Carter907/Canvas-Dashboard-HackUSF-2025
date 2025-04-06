from datetime import datetime
from zoneinfo import ZoneInfo

def convert_to_edt(dt: datetime) -> datetime:

    # Original UTC time
    utc_time = dt.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to EDT
    edt_time = utc_time.astimezone(ZoneInfo("America/New_York"))

    return datetime.strptime(edt_time.strftime("%Y-%m-%dT%I:%M:%S %p"), "%Y-%m-%dT%I:%M:%S %p")
