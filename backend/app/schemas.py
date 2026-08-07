from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VideoCreate(BaseModel):
    url: str


class VideoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    video_id: str
    title: str
    thumbnail_url: str
    created_at: datetime
