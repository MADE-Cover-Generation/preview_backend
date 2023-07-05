from typing import TYPE_CHECKING, List

import backend_app.models as _models
import backend_app.schemas.schema_request as _schema_request

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_request(
    request: _schema_request.CreateRequest, db: "Session"
) -> _schema_request.Request:
    request_dict = request.dict()
    request = _models.Request(**request_dict)
    db.add(request)
    db.commit()
    db.refresh(request)
    user_dict = {'telegram_id': request_dict['telegram_id']}
    user = _models.User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    video_dict = {'link': request_dict['link_to_video']}
    video = _models.Video(**video_dict)
    db.add(video)
    db.commit()
    db.refresh(video)
    return _schema_request.Request.from_orm(request)


async def get_all_requests(db: "Session") -> List[_schema_request.Request]:
    requests = db.query(_models.Request).all()
    return list(map(_schema_request.Request.from_orm, requests))


async def get_request(request_id: int, db: "Session"):
    request = db.query(_models.Request).filter(_models.Request.id == request_id).first()
    return request


async def delete_request(request: _models.Request, db: "Session"):
    db.delete(request)
    db.commit()
