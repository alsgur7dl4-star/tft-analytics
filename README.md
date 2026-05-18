# TFT Analytics

롤체지지 스타일의 TFT 전적 조회와 빅데이터 기반 추천 조합 분석 웹 서비스입니다.

## Local Setup

```powershell
copy .env.example .env
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env

docker-compose up -d db

cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

cd ..\frontend
npm install
npm run dev
```

새 프로젝트는 `tft_analytics_postgres` 컨테이너, `tft_analytics_db` DB, `tft_analytics_user` DB 유저, `tft_analytics_postgres_data` Docker volume만 사용합니다.
