import re
from urllib.parse import parse_qs, urlparse

import httpx

OEMBED_ENDPOINT = "https://www.youtube.com/oembed"

_VIDEO_ID_PATTERN = re.compile(r"^[\w-]{11}$")


class InvalidYouTubeUrlError(ValueError):
    """The given URL is not a resolvable YouTube video (bad format, private, deleted, ...)."""


class MetadataFetchError(RuntimeError):
    """YouTube's oEmbed endpoint could not be reached or returned an unexpected response."""


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")

    video_id: str | None = None
    if host == "youtu.be":
        video_id = parsed.path.lstrip("/")
    elif host in {"youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith(("/shorts/", "/embed/", "/live/")):
            video_id = parsed.path.split("/")[2]

    if not video_id or not _VIDEO_ID_PATTERN.match(video_id):
        raise InvalidYouTubeUrlError(f"'{url}'는 올바른 YouTube 링크가 아닙니다.")
    return video_id


def fetch_metadata(url: str) -> dict[str, str]:
    try:
        response = httpx.get(OEMBED_ENDPOINT, params={"url": url, "format": "json"}, timeout=5.0)
    except httpx.RequestError as exc:
        raise MetadataFetchError("YouTube에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.") from exc

    if response.status_code == 404:
        raise InvalidYouTubeUrlError("존재하지 않는 YouTube 영상입니다.")
    if response.status_code in (401, 403):
        raise InvalidYouTubeUrlError("비공개이거나 접근할 수 없는 영상입니다.")

    try:
        response.raise_for_status()
        data = response.json()
        return {"title": data["title"], "thumbnail_url": data["thumbnail_url"]}
    except (httpx.HTTPStatusError, KeyError, ValueError) as exc:
        raise MetadataFetchError("YouTube 영상 정보를 가져오지 못했습니다.") from exc
