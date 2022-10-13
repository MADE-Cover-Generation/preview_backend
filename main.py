from typing import TYPE_CHECKING, List
from urllib import request
import fastapi as _fastapi
import sqlalchemy.orm as _orm

import services.service_binder as _service_binder

import schemas.schema_video as _schema_video
import schemas.schema_preview as _schema_preview
import schemas.schema_user as _schema_user
import schemas.schema_request as _schema_request

import services.video_service as _video_service
import services.preview_service as _preview_service
import services.user_service as _user_service
import services.request_service as _request_service

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()


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
    video = await _video_service.get_random_video(telegram_id=telegram_id, db=db)
    if video is None:
        return []
    return await _preview_service.get_all_previews_by_link(video.link_to_video, db=db)


@app.post("/api/vote/")
async def vote_for_preview(
    preview: _schema_preview.CreatePreview,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    await _preview_service.vote_for_preview(preview.s3_key, db=db)
    return "succesfully voted"

@app.post("/api/user/mark_as_watched/")
async def mark_as_watched(
    user: _schema_user.CreateUser,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    await _user_service.mark_as_watched(user.telegram_id, user.watched_ids[0], db=db)
    return "succesfully marked"

# requests api
@app.post("/api/requests/", response_model=_schema_request.CreateRequest)
async def create_requests(
    request: _schema_request.CreateRequest,
    db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
):
    return await _request_service.create_request(request=request, db=db)


@app.get("/api/requests/", response_model=List[_schema_request.Request])
async def get_requests(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _request_service.get_all_requests(db=db)


# video api
# @app.post("/api/videos/", response_model=_schema_video.Video)
# async def create_video(
#     video: _schema_video.CreateVideo,
#     db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
# ):
#     return await _video_service.create_video(video=video, db=db)


@app.get("/api/video/", response_model=List[_schema_video.Video])
async def get_videos(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _video_service.get_all_videos(db=db)


# @app.get("/api/videos/{video_id}/", response_model=_schema_video.Video)
# async def get_video(
#     video_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     video = await _video_service.get_video(db=db, video_id=video_id)
#     if video is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Video does not exist")

#     return video


# @app.delete("/api/videos/{video_id}/")
# async def delete_video(
#     video_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     video = await _video_service.get_video(db=db, video_id=video_id)
#     if video is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Video does not exist")

#     await _video_service.delete_video(video, db=db)

#     return "successfully deleted the video"

# # preview api
# @app.post("/api/previews/", response_model=_schema_preview.Preview)
# async def create_preview(
#     preview: _schema_preview.CreatePreview,
#     db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
# ):
#     return await _preview_service.create_preview(preview=preview, db=db)


@app.get("/api/previews/", response_model=List[_schema_preview.Preview])
async def get_previews(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _preview_service.get_all_previews(db=db)


# @app.get("/api/previews/{preview_id}/", response_model=_schema_preview.Preview)
# async def get_preview(
#     preview_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     preview = await _preview_service.get_preview(db=db, preview_id=preview_id)
#     if preview is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Preview does not exist")

#     return preview


# @app.delete("/api/previews/{preview_id}/")
# async def delete_preview(
#     preview_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     preview = await _preview_service.get_preview(db=db, preview_id=preview_id)
#     if preview is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Preview does not exist")

#     await _preview_service.delete_preview(preview, db=db)

#     return "successfully deleted the preview"


# # user api
# @app.post("/api/user/", response_model=_schema_user.User)
# async def create_user(
#     user: _schema_user.CreateUser,
#     db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
# ):
#     return await _user_service.create_user(user=user, db=db)


@app.get("/api/user/", response_model=List[_schema_user.User])
async def get_users(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
    return await _user_service.get_all_users(db=db)


# @app.get("/api/user/{user_id}/", response_model=_schema_user.User)
# async def get_user(
#     user_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     user = await _user_service.get_user(db=db, user_id=user_id)
#     if user is None:
#         raise _fastapi.HTTPException(status_code=404, detail="User does not exist")

#     return user


# @app.delete("/api/user/{user_id}/")
# async def delete_user(
#     user_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     user = await _user_service.get_user(db=db, user_id=user_id)
#     if user is None:
#         raise _fastapi.HTTPException(status_code=404, detail="User does not exist")

#     await _user_service.delete_user(user, db=db)

#     return "successfully deleted the user"


# # requests api
# @app.post("/api/requests/", response_model=_schema_request.CreateRequest)
# async def create_requests(
#     request: _schema_request.CreateRequest,
#     db: _orm.Session = _fastapi.Depends(_service_binder.get_db),
# ):
#     return await _request_service.create_request(request=request, db=db)


# @app.get("/api/requests/", response_model=List[_schema_request.Request])
# async def get_requests(db: _orm.Session = _fastapi.Depends(_service_binder.get_db)):
#     return await _request_service.get_all_requests(db=db)


# @app.get("/api/requests/{request_id}/", response_model=_schema_request.Request)
# async def get_request(
#     request_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     request = await _request_service.get_request(db=db, request_id=request_id)
#     if request is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Request does not exist")

#     return request


# @app.delete("/api/requests/{request_id}/")
# async def delete_request(
#     request_id: int, db: _orm.Session = _fastapi.Depends(_service_binder.get_db)
# ):
#     request = await _request_service.get_request(db=db, request_id=request_id)
#     if request is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Request does not exist")

#     await _request_service.delete_request(request, db=db)

#     return "successfully deleted the request"
