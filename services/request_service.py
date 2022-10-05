from typing import TYPE_CHECKING, List
from urllib import request

import models as _models
import schemas.schema_request as _schema_request

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_request(
    request: _schema_request.CreateRequest, db: "Session"
) -> _schema_request.Request:
    request = _models.Request(**request.dict())
    db.add(request)
    db.commit()
    db.refresh(request)
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