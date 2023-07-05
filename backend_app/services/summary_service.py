from typing import TYPE_CHECKING, List

import backend_app.models as _models
import backend_app.schemas.schema_summary as _schema_summary
import backend_app.converters as _converters

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

async def create_summary(
    summary: _schema_summary.CreateSummary, db: "Session"
) -> _schema_summary.Summary:
    summary = _models.Summary(**summary.dict())
    
    video = db.query(_models.Video).filter(_models.Video.link_to_video == summary.link_to_video).first()
    if video == None:
        video = _converters.convert_summary_to_video(summary)
        db.add(video)
        db.commit()
        db.refresh(video)

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return _schema_summary.Summary.from_orm(summary)

async def vote_for_summary(
    s3_key: str, db: "Session"
) -> _schema_summary.Summary:
    summary = db.query(_models.Summary).filter(_models.Summary.s3_key == s3_key).first()
    summary.votes += 1
    db.commit()
    db.refresh(summary)
    return _schema_summary.Summary.from_orm(summary)

async def get_all_summaries(db: "Session") -> List[_schema_summary.Summary]:
    summaries = db.query(_models.Summary).all()
    return list(map(_schema_summary.Summary.from_orm, summaries))

async def get_summary(summary_id: int, db: "Session"):
    summary = db.query(_models.Summary).filter(_models.Summary.id == summary_id).first()
    return summary

async def get_all_summaries_by_link(link_to_video: str, db: "Session") -> List[_schema_summary.Summary]:
    summaries = db.query(_models.Summary).filter(_models.Summary.link_to_video == link_to_video)
    return list(map(_schema_summary.Summary.from_orm, summaries))

async def wipe_all_summaries(db: "Session"):
    summaries = db.query(_models.Summary).all()
    for summary in summaries:
        db.delete(summary)
    db.commit()

async def delete_summaries(summary: _models.Summary, db: "Session"):
    db.delete(summary)
    db.commit()
