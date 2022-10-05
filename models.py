import sqlalchemy as _sql

import database as _database

class Video(_database.Base):
    __tablename__ = "videos"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    link = _sql.Column(_sql.String, unique=True)

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    telegram_id = _sql.Column(_sql.String)
    
class Preview(_database.Base):
    __tablename__ = "previews"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    type = _sql.Column(_sql.String, unique=True)
    link_to_video = _sql.Column(_sql.String)
    s3_key = _sql.Column(_sql.String, unique=True)


class Request(_database.Base):
    __tablename__ = "requests"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    telegram_id = _sql.Column(_sql.String)
    link_to_video = _sql.Column(_sql.String)
    link_to_preview = _sql.Column(_sql.String)




