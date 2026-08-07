# practice-project

AI 바이브 코딩 학습을 위한 연습용 프로젝트입니다.

## 현재 상태

백엔드(FastAPI)와 프론트엔드(Next.js)의 기본 뼈대가 생성되었습니다.

## 프로젝트 구조

```
.
├── backend/    # FastAPI 백엔드
│   ├── app/
│   │   └── main.py
│   └── requirements.txt
└── frontend/   # Next.js 프론트엔드 (TypeScript, App Router)
```

## 실행 방법

### 백엔드

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

`GET /health` 요청 시 `{"status": "ok"}` 응답을 확인할 수 있습니다.

### 프론트엔드

```bash
cd frontend
npm install
npm run dev
```

`http://localhost:3000` 에서 확인할 수 있습니다.

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
