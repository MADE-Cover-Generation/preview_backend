from typing import TYPE_CHECKING, List

import models as _models
import schemas.schema_video as _schema_video

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_video(
    video: _schema_video.CreateVideo, db: "Session"
) -> _schema_video.Video:
    video = _models.Video(**video.dict())
    db.add(video)
    db.commit()
    db.refresh(video)
    return _schema_video.Video.from_orm(video)


async def get_all_videos(db: "Session") -> List[_schema_video.Video]:
    videos = db.query(_models.Video).all()
    return list(map(_schema_video.Video.from_orm, videos))


async def get_video(video_id: int, db: "Session"):
    video = db.query(_models.Video).filter(_models.Video.id == video_id).first()
    return video


async def delete_video(video: _models.Video, db: "Session"):
    db.delete(video)
    db.commit()