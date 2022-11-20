import backend_app.schemas.schema_preview as _schema_preview
import backend_app.schemas.schema_summary as _schema_summary
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as _sql
 
import backend_app.models as _models


def convert_preview_to_video(preview: _schema_preview.CreatePreview):
    return _models.Video(**{'link_to_video': preview.link_to_video, 'type': 'preview'})


def convert_summary_to_video(summary: _schema_summary.CreateSummary):
    return _models.Video(**{'link_to_video': summary.link_to_video, 'type': 'summary'})


def convert_id_to_user(telegram_id: str):
    return _models.User(**{'telegram_id': telegram_id, 'watched_ids': list()})

