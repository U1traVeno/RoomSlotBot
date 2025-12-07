from contextlib import asynccontextmanager
from fastapi import FastAPI
from pingslot.config import settings
from pingslot.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.server.api_prefix}/openapi.json",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Welcome to PingSlot"}
