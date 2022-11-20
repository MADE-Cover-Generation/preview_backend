import datetime as _dt
import pydantic as _pydantic

class _BaseSummary(_pydantic.BaseModel):
    type: str
    link_to_video: str
    s3_key: str
    votes: int

class Summary(_BaseSummary):
    id: int

    class Config:
        orm_mode = True

class CreateSummary(_BaseSummary):
    pass