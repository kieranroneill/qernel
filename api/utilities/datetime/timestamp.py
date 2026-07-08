from datetime import datetime, timezone


def timestamp() -> str:
    """
    Creates an ISO 8601 date string in UTC to milliseconds precision.

    Returns:
        (str): A ISO 8601 date string in UTC to milliseconds precision.
    """
    now = datetime.now(timezone.utc)
    date = now.replace(microsecond=now.microsecond % 1000)  # truncate to milliseconds

    return date.isoformat().replace("+00:00", "Z")
