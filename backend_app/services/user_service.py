from typing import TYPE_CHECKING, List

import backend_app.models as _models
import backend_app.schemas.schema_user as _schema_user

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

async def create_user(
    user: _schema_user.CreateUser, db: "Session"
) -> _schema_user.User:
    user = _models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return _schema_user.User.from_orm(user)

async def mark_as_watched(
    telegram_id: str, link_to_url: str, db: "Session"
) -> _schema_user.User:
    user = db.query(_models.User).filter(_models.User.telegram_id == telegram_id).first()
    new_ids = list(user.watched_ids)
    
    if link_to_url == None or link_to_url == "null" or link_to_url in new_ids:
        return None

    new_ids.append(link_to_url)
    user.watched_ids = new_ids 
    db.commit()
    db.refresh(user)
    return user

async def get_all_users(db: "Session") -> List[_schema_user.User]:
    users = db.query(_models.User).all()
    return list(map(_schema_user.User.from_orm, users))

async def wipe_all_users(db: "Session"):
    users = db.query(_models.User).all()
    for user in users:
        db.delete(user)
    db.commit()

async def get_user(user_id: int, db: "Session"):
    user = db.query(_models.User).filter(_models.User.id == user_id).first()
    return user

async def delete_user(user: _models.User, db: "Session"):
    db.delete(user)
    db.commit()
