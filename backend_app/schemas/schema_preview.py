import datetime as _dt
import pydantic as _pydantic


class _BasePreview(_pydantic.BaseModel):
    type: str
    link_to_video: str
    s3_key: str
    votes: int


class Preview(_BasePreview):
    id: int

    class Config:
        orm_mode = True


class CreatePreview(_BasePreview):
    pass
    
