from flask import Blueprint
from sqlalchemy import func
from app.extensions import db
from app.utils.responses import ok

bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    db.session.execute(db.select(func.now()))
    return ok({"status": "healthy"})
