import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas, youtube
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="practice-project API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/videos", response_model=list[schemas.VideoOut])
def list_videos(db: Session = Depends(get_db)) -> list[models.Video]:
    return list(db.scalars(select(models.Video).order_by(models.Video.created_at.desc())))


@app.post("/videos", response_model=schemas.VideoOut, status_code=201)
def create_video(payload: schemas.VideoCreate, db: Session = Depends(get_db)) -> models.Video:
    try:
        video_id = youtube.extract_video_id(payload.url)
    except youtube.InvalidYouTubeUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        metadata = youtube.fetch_metadata(payload.url)
    except youtube.InvalidYouTubeUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except youtube.MetadataFetchError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    video = models.Video(url=payload.url, video_id=video_id, **metadata)
    db.add(video)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="이미 저장된 영상입니다.") from exc
    db.refresh(video)
    return video
