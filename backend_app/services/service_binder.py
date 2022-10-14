from typing import TYPE_CHECKING, List

import backend_app.database as _database
import backend_app.models as _models

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

_add_tables()