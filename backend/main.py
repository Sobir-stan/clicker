from fastapi import FastAPI

from backend.api.router import router

app = FastAPI(title="Clicker Game")

app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "ok"}
