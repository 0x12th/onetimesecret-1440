from fastapi import FastAPI

from src.secret.router import router as secret_router

app = FastAPI()

app.include_router(secret_router)


@app.get("/")
async def main() -> str:
    return "foo"
