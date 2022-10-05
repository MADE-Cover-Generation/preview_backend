import datetime as _dt
import pydantic as _pydantic

class _BaseUser(_pydantic.BaseModel):
    telegram_id: str

class User(_BaseUser):
    id: int

    class Config:
        orm_mode = True

class CreateUser(_BaseUser):
    pass