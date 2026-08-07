# practice-project

AI 바이브 코딩 학습을 위한 연습용 프로젝트입니다.

## 현재 상태

유튜브 영상 링크를 저장하고 모아볼 수 있는 기능(KAN-3 MVP)이 구현되어 있습니다.

## 프로젝트 구조

```
.
├── backend/    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py       # /health, /videos 엔드포인트
│   │   ├── models.py     # SQLAlchemy Video 모델
│   │   ├── schemas.py    # Pydantic 스키마
│   │   ├── youtube.py    # YouTube URL 파싱 및 oEmbed 메타데이터 조회
│   │   └── database.py   # SQLite 세션 설정
│   └── requirements.txt
└── frontend/   # Next.js 프론트엔드 (TypeScript, App Router)
    ├── app/page.tsx       # 영상 저장 폼 + 목록 화면
    └── lib/api.ts         # 백엔드 API 클라이언트
```

## 실행 방법

### 백엔드

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- `GET /health` → `{"status": "ok"}`
- `GET /videos` → 저장된 영상 목록 조회
- `POST /videos` (`{"url": "https://www.youtube.com/watch?v=..."}`) → 영상 링크 저장 (제목/썸네일은 YouTube oEmbed API로 자동 조회)

데이터는 `backend/app.db` (SQLite)에 저장됩니다.

### 프론트엔드

```bash
cd frontend
cp .env.example .env.local   # 필요 시 NEXT_PUBLIC_API_BASE_URL 조정
npm install
npm run dev
```

`http://localhost:3000` 에서 확인할 수 있습니다. (백엔드가 8000번 포트에서 함께 실행 중이어야 합니다.)

## 다음 할 일

**2026-08-15까지 상세 개발 계획을 수립합니다.** (기준일: 2026-08-08, 일주일 이내)

수립할 항목:

- [ ] 프로젝트 목표 및 범위 정의
- [ ] 기술 스택 선정
- [ ] 주요 기능 목록 및 우선순위
- [ ] 개발 일정 / 마일스톤
- [ ] 프로젝트 구조 설계

계획이 확정되면 이 문서의 내용을 개요, 설치·실행 방법, 프로젝트 구조로 대체합니다.

## 관련 이슈

- #1 README.md 추가 필요
- KAN-2 웹앱 프로젝트 뼈대 생성 필요
- KAN-3 유튜브 영상 저장 기능 개발 (MVP: 저장/목록 조회)
