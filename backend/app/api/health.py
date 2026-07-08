from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import DB_PATH, get_db
from app.models import AppMeta

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health")
def health(db: DbSession):
    error = None
    initialized_at = None

    try:
        db.execute(text("SELECT 1"))

        meta = db.get(AppMeta, "db_initialized")

        if meta is None:
            meta = AppMeta(key="db_initialized", value="true")
            db.add(meta)
            db.commit()
            db.refresh(meta)

        initialized_at = meta.created_at

        return {
            "ok": True,
            "sqlite": {
                "ok": True,
                "path": str(DB_PATH),
                "exists": DB_PATH.exists(),
                "initialized_at": initialized_at,
            },
        }

    except Exception as exc:
        error = str(exc)

        return {
            "ok": False,
            "sqlite": {
                "ok": False,
                "path": str(DB_PATH),
                "exists": DB_PATH.exists(),
                "error": error,
            },
        }
