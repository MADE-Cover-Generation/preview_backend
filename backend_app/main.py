import os

from typing import TYPE_CHECKING, List
import fastapi as _fastapi
import sqlalchemy.orm as _orm

import backend_app.database as _database

import backend_app.services.service_binder as _service_binder

import backend_app.schemas.schema_video as _schema_video
import backend_app.schemas.schema_preview as _schema_preview
import backend_app.schemas.schema_user as _schema_user
import backend_app.schemas.schema_request as _schema_request
import backend_app.schemas.schema_summary as _schema_summary

import backend_app.services.video_service as _video_service
import backend_app.services.preview_service as _preview_service
import backend_app.services.user_service as _user_service
import backend_app.services.request_service as _request_service
import backend_app.services.summary_service as _summary_service
import dotenv

dotenv.load_dotenv()

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI(title = "Backend preview")

@app.get("/")
def read_root():
    return {"it's": "alive"}

@app.post("/api/preview/create/", response_model=_schema_preview.CreatePreview)
async def create_preview(
    preview: _schema_preview.CreatePreview,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    return await _preview_service.create_preview(preview=preview, db=db)


@app.get("/api/preview/{telegram_id}", response_model=List[_schema_preview.CreatePreview])
async def get_preview_for_vote(
    telegram_id: str,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    video = await _video_service.get_random_video(telegram_id=telegram_id, db=db, type="preview")
    if video is None:
        return []
    return await _preview_service.get_all_previews_by_link(video.link_to_video, db=db)


@app.post("/api/preview/vote_for/")
async def vote_for_preview(
    preview: _schema_preview.CreatePreview,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    await _preview_service.vote_for_preview(preview.s3_key, db=db)
    return "succesfully voted"


@app.get("/api/previews/", response_model=List[_schema_preview.Preview])
async def get_previews(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _preview_service.get_all_previews(db=db)


@app.delete("/api/preview/")
async def wipe_all_previews(master_password: str, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    if master_password == os.getenv('master_password'):
        await _preview_service.wipe_all_previews(db=db)
        return "PREVIEWS ARE DELETED"


@app.post("/api/summary/create/", response_model=_schema_summary.CreateSummary)
async def create_summary(
    summary: _schema_summary.CreateSummary,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    return await _summary_service.create_summary(summary=summary, db=db)


@app.get("/api/summary/{telegram_id}", response_model=List[_schema_summary.CreateSummary])
async def get_summary_for_vote(
    telegram_id: str,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    video = await _video_service.get_random_video(telegram_id=telegram_id, db=db, type="summary")
    if video is None:
        return []
    return await _summary_service.get_all_summaries_by_link(video.link_to_video, db=db)


@app.post("/api/summary/vote_for/")
async def vote_for_summary(
    summary: _schema_summary.CreateSummary,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    await _summary_service.vote_for_summary(summary.s3_key, db=db)
    return "succesfully voted for summary"


@app.get("/api/summaries/", response_model=List[_schema_summary.Summary])
async def get_summaries(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _summary_service.get_all_summaries(db=db)


@app.delete("/api/summaries/")
async def wipe_all_summaries(master_password: str, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    if master_password == os.getenv('master_password'):
        await _summary_service.wipe_all_summaries(db=db)
        return "SUMMARIES ARE DELETED"


@app.get("/api/video/", response_model=List[_schema_video.Video])
async def get_videos(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _video_service.get_all_videos(db=db)


@app.delete("/api/videos/")
async def wipe_all_videos(master_password: str, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    if master_password == os.getenv('master_password'):
        await _video_service.wipe_all_videos(db=db)
        return "VIDEOS ARE DELETED"


@app.get("/api/user/", response_model=List[_schema_user.User])
async def get_users(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _user_service.get_all_users(db=db)


@app.delete("/api/user/")
async def wipe_all_users(master_password: str, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    if master_password == os.getenv('master_password'):
        await _user_service.wipe_all_users(db=db)
        return "USERS ARE DELETED"


@app.post("/api/user/mark_as_watched/")
async def mark_as_watched(
    user: _schema_user.CreateUser,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    return await _user_service.mark_as_watched(user.telegram_id, user.watched_ids[0], db=db)

@app.post("/api/requests/", response_model=_schema_request.CreateRequest)
async def create_requests(
    request: _schema_request.CreateRequest,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    return await _request_service.create_request(request=request, db=db)


@app.get("/api/requests/", response_model=List[_schema_request.Request])
async def get_requests(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _request_service.get_all_requests(db=db)


@app.get("/api/wipe_all/")
async def wipe_all(master_password: str, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    if master_password == os.getenv('master_password'):
        await _user_service.wipe_all_users(db=db)
        await _preview_service.wipe_all_previews(db=db)
        await _video_service.wipe_all_videos(db=db)
        await _summary_service.wipe_all_summaries(db=db)
        
