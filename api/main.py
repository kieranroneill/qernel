import logging
import os

import uvicorn


def main() -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=os.getenv("LOG_LEVEL", "INFO").upper())

    uvicorn.run(
        "api.app:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "3000")),
        reload=os.getenv("API_RELOAD", "false").lower() == "true",
    )


if __name__ == "__main__":
    main()
