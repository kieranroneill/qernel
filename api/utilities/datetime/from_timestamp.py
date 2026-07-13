from datetime import datetime, timezone


def from_timestamp(timestamp: int) -> datetime:
    """
    Convert a Unix timestamp to a timezone-aware UTC datetime.

    The returned datetime is normalized to UTC and has microseconds removed,
    so it is safe to serialize as ISO 8601 with second precision.

    Args:
        timestamp (int): Unix timestamp in seconds.

    Returns:
       (datetime): A timezone-aware datetime in UTC with microseconds set to 0.
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0)
