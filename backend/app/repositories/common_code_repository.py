from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.common import CommonCode, CommonCodeGroup


class CommonCodeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_groups(self) -> list[CommonCodeGroup]:
        return list(self.db.scalars(select(CommonCodeGroup).order_by(CommonCodeGroup.group_key.asc())))

    def get_group_by_key(self, group_key: str) -> CommonCodeGroup | None:
        return self.db.scalar(select(CommonCodeGroup).where(CommonCodeGroup.group_key == group_key))

    def create_group(self, group_key: str, group_name: str, description: str | None = None) -> CommonCodeGroup:
        group = CommonCodeGroup(group_key=group_key, group_name=group_name, description=description)
        self.db.add(group)
        self.db.flush()
        return group

    def delete_group(self, group: CommonCodeGroup) -> None:
        self.db.delete(group)
        self.db.flush()

    def list_codes(self, group_id: int) -> list[CommonCode]:
        return list(
            self.db.scalars(
                select(CommonCode)
                .where(CommonCode.group_id == group_id)
                .order_by(CommonCode.sort_order.asc(), CommonCode.id.asc())
            )
        )

    def create_code(
        self,
        group_id: int,
        code: str,
        label: str,
        sort_order: int = 0,
        meta_json: dict | None = None,
    ) -> CommonCode:
        common_code = CommonCode(
            group_id=group_id, code=code, label=label, sort_order=sort_order, meta_json=meta_json
        )
        self.db.add(common_code)
        self.db.flush()
        return common_code

    def get_code(self, code_id: int) -> CommonCode | None:
        return self.db.get(CommonCode, code_id)

    def delete_code(self, code: CommonCode) -> None:
        self.db.delete(code)
        self.db.flush()
