from datetime import datetime, timezone


def to_iso_string(dt: datetime) -> str:
    """
    Convert a datetime to an ISO 8601 UTC string with second precision.

    The datetime is first normalized to UTC, then truncated to whole seconds.

    Args:
        dt (datetime): A datetime object, timezone-aware or naive.

    Returns:
        str: An ISO 8601 formatted UTC string with second precision.
    """
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()
