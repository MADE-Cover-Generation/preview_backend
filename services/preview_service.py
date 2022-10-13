from typing import TYPE_CHECKING, List

import models as _models
import schemas.schema_preview as _schema_preview
import converters

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_preview(
    preview: _schema_preview.CreatePreview, db: "Session"
) -> _schema_preview.Preview:
    preview = _models.Preview(**preview.dict())
    
    db.add(preview)
    db.commit()
    db.refresh(preview)

    video = db.query(_models.Video).filter(_models.Video.link_to_video == preview.link_to_video).first()
    if video == None:
        video = converters.convert_preview_to_video(preview)
        db.add(video)
        db.commit()
        db.refresh(video)

    return _schema_preview.Preview.from_orm(preview)


async def vote_for_preview(
    s3_key: str, db: "Session"
) -> _schema_preview.Preview:
    preview = db.query(_models.Preview).filter(_models.Preview.s3_key == s3_key).first()
    preview.votes += 1
    db.commit()
    db.refresh(preview)
    return _schema_preview.Preview.from_orm(preview)


async def get_all_previews(db: "Session") -> List[_schema_preview.Preview]:
    previews = db.query(_models.Preview).all()
    return list(map(_schema_preview.Preview.from_orm, previews))


async def get_all_previews_by_link(link_to_video: str, db: "Session") -> List[_schema_preview.Preview]:
    previews = db.query(_models.Preview).filter(_models.Preview.link_to_video == link_to_video)
    return list(map(_schema_preview.Preview.from_orm, previews))


async def get_preview(preview_id: int, db: "Session"):
    preview = db.query(_models.Preview).filter(_models.Preview.id == preview_id).first()
    return preview


async def delete_preview(preview: _models.Preview, db: "Session"):
    db.delete(preview)
    db.commit()