import logging
import os

import uvicorn


def main() -> None:
    log_level = os.getenv("LOG_LEVEL", "ERROR")

    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level.upper())
    uvicorn.run(
        "api.app:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        log_level=log_level.lower(),
        port=int(os.getenv("API_PORT", "3000")),
        reload=os.getenv("API_RELOAD", "false").lower() == "true",
    )


if __name__ == "__main__":
    main()
