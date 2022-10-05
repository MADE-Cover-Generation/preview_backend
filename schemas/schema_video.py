import datetime as _dt
import pydantic as _pydantic

class _BaseVideo(_pydantic.BaseModel):
    link: str

class Video(_BaseVideo):
    id: int

    class Config:
        orm_mode = True

class CreateVideo(_BaseVideo):
    pass