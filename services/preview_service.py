from typing import TYPE_CHECKING, List

import models as _models
import schemas.schema_preview as _schema_preview

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_preview(
    preview: _schema_preview.CreatePreview, db: "Session"
) -> _schema_preview.Preview:
    preview = _models.Preview(**preview.dict())
    db.add(preview)
    db.commit()
    db.refresh(preview)
    return _schema_preview.Preview.from_orm(preview)


async def get_all_previews(db: "Session") -> List[_schema_preview.Preview]:
    previews = db.query(_models.Preview).all()
    return list(map(_schema_preview.Preview.from_orm, previews))


async def get_preview(preview_id: int, db: "Session"):
    preview = db.query(_models.Preview).filter(_models.Preview.id == preview_id).first()
    return preview


async def delete_preview(preview: _models.Preview, db: "Session"):
    db.delete(preview)
    db.commit()