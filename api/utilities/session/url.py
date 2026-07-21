import os


def url() -> str:
    db = os.environ.get("REDIS_DB", "0")
    host = os.environ["REDIS_HOST"]
    password = os.environ["REDIS_PASSWORD"]
    port = os.environ.get("REDIS_PORT", "6379")
    username = os.environ["REDIS_USERNAME"]

    return f"redis://{username}:{password}@{host}:{port}/{db}"
