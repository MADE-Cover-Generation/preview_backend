from typing import TYPE_CHECKING, List

import backend_app.models as _models
import backend_app.schemas.schema_video as _schema_video
import backend_app.converters


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


async def get_random_video(
    telegram_id: str, db: "Session"
) -> _schema_video.Video:
    user = db.query(_models.User).filter(_models.User.telegram_id == telegram_id).first()
    if user == None:
        user = converters.convert_id_to_user(telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    watched_ids = user.watched_ids
    video = db.query(_models.Video).filter(~_models.Video.link_to_video.in_(watched_ids)).first()
    if video is None:
        return None
    return _schema_video.Video.from_orm(video)


async def get_all_videos(db: "Session") -> List[_schema_video.Video]:
    videos = db.query(_models.Video).all()
    return list(map(_schema_video.Video.from_orm, videos))


async def get_video(video_id: int, db: "Session"):
    video = db.query(_models.Video).filter(_models.Video.id == video_id).first()
    return video


async def get_video(video_id: int, db: "Session"):
    video = db.query(_models.Video).filter(_models.Video.id == video_id).first()
    return video

async def wipe_all_videos(db: "Session"):
    videos = db.query(_models.Video).all()
    for video in videos:
        db.delete(video)
    db.commit()

async def delete_video(video: _models.Video, db: "Session"):
    db.delete(video)
    db.commit()