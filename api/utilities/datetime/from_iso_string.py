from datetime import datetime, timezone


def from_iso_string(iso_string: str) -> datetime:
    """
    Convert a UTC datetime string to a timezone-aware UTC datetime.

    The returned datetime is normalized to UTC and has microseconds removed,
    so it is safe to serialize as ISO 8601 with second precision.

    Args:
        iso_string (str): Datetime string in UTC, with second precision.

    Returns:
        datetime: A timezone-aware datetime in UTC with microseconds set to 0.
    """
    return datetime.fromisoformat(iso_string).replace(tzinfo=timezone.utc, microsecond=0)
