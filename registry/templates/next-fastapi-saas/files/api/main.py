from fastapi import FastAPI

app = FastAPI(title="Generated Project API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
