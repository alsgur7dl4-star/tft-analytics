"""
Season 17 신(God) 목록 시드 스크립트.

실행 방법:
    cd backend
    python -m scripts.seed_season17_gods

신 목록(GODS)에 실제 Season 17 신들을 채워 넣으세요.
각 항목의 형식:
    {
        "god_key":    "API에서 사용하는 고유 키 (ex: God_Lux)",
        "god_name":   "표시 이름 (ex: 럭스)",
        "description":"신의 전체 설명",
        "passive_desc":"패시브 효과 요약",
        "set_name":   "17",      # 현재 시즌 번호
        "sort_order": 0,          # 표시 순서 (낮을수록 위)
    }
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_engine
from app.models.tft import TftStaticGod
from sqlalchemy.orm import Session

SET_NAME = "17"

# ──────────────────────────────────────────────
# 아래 목록에 Season 17 신들을 채워 넣으세요.
# ──────────────────────────────────────────────
GODS: list[dict] = [
    # 예시 형식 (실제 Season 17 신 이름으로 교체하세요):
    # {
    #     "god_key": "God_Example1",
    #     "god_name": "신1",
    #     "description": "이 신을 선택하면 ...",
    #     "passive_desc": "패시브: ...",
    #     "set_name": SET_NAME,
    #     "sort_order": 0,
    # },
]
# ──────────────────────────────────────────────


def seed(db: Session) -> None:
    if not GODS:
        print("[seed_season17_gods] GODS 목록이 비어 있습니다. 스크립트 상단에 신 목록을 채워 주세요.")
        return

    upserted = 0
    for g in GODS:
        existing = db.scalar(select(TftStaticGod).where(TftStaticGod.god_key == g["god_key"]))
        if existing:
            existing.god_name = g["god_name"]
            existing.description = g.get("description")
            existing.passive_desc = g.get("passive_desc")
            existing.set_name = g.get("set_name", SET_NAME)
            existing.sort_order = g.get("sort_order", 0)
        else:
            db.add(
                TftStaticGod(
                    god_key=g["god_key"],
                    god_name=g["god_name"],
                    description=g.get("description"),
                    passive_desc=g.get("passive_desc"),
                    set_name=g.get("set_name", SET_NAME),
                    sort_order=g.get("sort_order", 0),
                )
            )
        upserted += 1

    db.commit()
    print(f"[seed_season17_gods] {upserted}개 신 등록/업데이트 완료 (set_name={SET_NAME})")


if __name__ == "__main__":
    engine = get_engine(settings.database_url)
    with Session(engine) as db:
        seed(db)
