import datetime as _dt
import pydantic as _pydantic


class _BaseRequest(_pydantic.BaseModel):
    telegram_id: str
    link_to_video: str


class Request(_BaseRequest):
    id: int

    class Config:
        orm_mode = True


class CreateRequest(_BaseRequest):
    pass
