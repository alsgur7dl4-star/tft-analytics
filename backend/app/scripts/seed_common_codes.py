"""공통코드 초기 데이터 등록 스크립트.

실행: python -m app.scripts.seed_common_codes
"""

from app.core.database import SessionLocal
from app.models.common import CommonCode, CommonCodeGroup
from sqlalchemy import select

SEED_DATA = {
    "TIER_LABEL": {
        "group_name": "조합 티어 라벨",
        "description": "메타 조합 티어 등급 (점수 상위 순)",
        "codes": [
            {"code": "S", "label": "S티어", "sort_order": 1},
            {"code": "A", "label": "A티어", "sort_order": 2},
            {"code": "B", "label": "B티어", "sort_order": 3},
            {"code": "C", "label": "C티어", "sort_order": 4},
            {"code": "D", "label": "D티어", "sort_order": 5},
        ],
    },
    "JOB_LOG_LEVEL": {
        "group_name": "배치 로그 레벨",
        "description": "배치 잡 스텝 로그 심각도",
        "codes": [
            {"code": "INFO", "label": "정보", "sort_order": 1},
            {"code": "WARN", "label": "경고", "sort_order": 2},
            {"code": "ERROR", "label": "오류", "sort_order": 3},
        ],
    },
    "JOB_STATUS": {
        "group_name": "배치 잡 상태",
        "description": "배치 잡 실행 상태 코드",
        "codes": [
            {"code": "PENDING", "label": "대기중", "sort_order": 1},
            {"code": "RUNNING", "label": "실행중", "sort_order": 2},
            {"code": "SUCCESS", "label": "성공", "sort_order": 3},
            {"code": "FAILED", "label": "실패", "sort_order": 4},
        ],
    },
    "REGION": {
        "group_name": "서버 지역",
        "description": "Riot API 서버 지역 코드",
        "codes": [
            {"code": "KR", "label": "한국", "sort_order": 1},
            {"code": "NA", "label": "북미", "sort_order": 2},
            {"code": "EUW", "label": "서유럽", "sort_order": 3},
            {"code": "EUNE", "label": "북동유럽", "sort_order": 4},
        ],
    },
    "COMP_DIFFICULTY": {
        "group_name": "조합 난이도",
        "description": "조합 실행 난이도 등급",
        "codes": [
            {"code": "EASY", "label": "쉬움", "sort_order": 1},
            {"code": "MEDIUM", "label": "보통", "sort_order": 2},
            {"code": "HIGH", "label": "어려움", "sort_order": 3},
        ],
    },
}


def seed() -> None:
    with SessionLocal() as db:
        for group_key, meta in SEED_DATA.items():
            group = db.scalar(select(CommonCodeGroup).where(CommonCodeGroup.group_key == group_key))
            if not group:
                group = CommonCodeGroup(
                    group_key=group_key,
                    group_name=meta["group_name"],
                    description=meta["description"],
                )
                db.add(group)
                db.flush()
                print(f"[CREATE] 그룹: {group_key}")
            else:
                print(f"[SKIP]   그룹 이미 존재: {group_key}")

            for code_meta in meta["codes"]:
                exists = db.scalar(
                    select(CommonCode).where(
                        CommonCode.group_id == group.id,
                        CommonCode.code == code_meta["code"],
                    )
                )
                if not exists:
                    db.add(
                        CommonCode(
                            group_id=group.id,
                            code=code_meta["code"],
                            label=code_meta["label"],
                            sort_order=code_meta["sort_order"],
                        )
                    )
                    print(f"         코드 추가: {code_meta['code']} ({code_meta['label']})")

        db.commit()
        print("\n공통코드 시드 완료.")


if __name__ == "__main__":
    seed()
