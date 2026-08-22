from contextlib import asynccontextmanager

from fastapi import FastAPI
from chainlit.utils import mount_chainlit

from api.routes.documents import router as documents_router
from database.session import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize application database tables
    await init_database()

    yield


app = FastAPI(
    title="AI Knowledge Assistant API",
    lifespan=lifespan,
)


app.include_router(
    documents_router,
    prefix="/api",
)


@app.get("/")
def home():
    return {
        "message": "AI Knowledge Assistant API is running"
    }


mount_chainlit(
    app=app,
    target="ui/chainlit_app.py",
    path="/chainlit",
)