from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes import router
from db.init_db import init_models

# Used to manage startup + shutdown lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_models()
    yield
    # shutdown (optional cleanup)

app = FastAPI(
    title="Advanced LLM API",
    lifespan=lifespan
)

app.include_router(router)