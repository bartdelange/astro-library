from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.astro_objects import router as astro_objects_router
from app.api.files import router as files_router
from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.api.sessions import router as sessions_router
from app.config import settings
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(astro_objects_router, prefix="/api")
app.include_router(files_router, prefix="/api")
app.include_router(health_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")

frontend_dist = settings.frontend_dist

if frontend_dist.exists():
    assets_dir = frontend_dist / "assets"

    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        return FileResponse(frontend_dist / "index.html")
