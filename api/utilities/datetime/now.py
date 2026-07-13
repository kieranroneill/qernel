from datetime import datetime, timezone


def now() -> datetime:
    """
    Return the current UTC datetime with second precision.

    The returned datetime is timezone-aware, uses UTC, and has microseconds
    removed so it can be serialized consistently in ISO 8601 format.

    Returns:
        (datetime): A timezone-aware datetime in UTC with microseconds set to 0.
    """
    return datetime.now(timezone.utc).replace(microsecond=0)
