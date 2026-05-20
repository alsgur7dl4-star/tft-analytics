from fastapi import status
from sqlalchemy.orm import Session

from app.core import error_codes
from app.core.exceptions import AppException
from app.repositories.common_code_repository import CommonCodeRepository
from app.schemas.admin import CommonCodeGroupResponse, CommonCodeResponse


class CommonCodeService:
    def __init__(self, db: Session):
        self.repo = CommonCodeRepository(db)
        self.db = db

    def list_groups(self) -> list[CommonCodeGroupResponse]:
        groups = self.repo.list_groups()
        result = []
        for group in groups:
            codes = self.repo.list_codes(group.id)
            result.append(
                CommonCodeGroupResponse(
                    id=group.id,
                    group_key=group.group_key,
                    group_name=group.group_name,
                    description=group.description,
                    codes=[CommonCodeResponse.model_validate(c, from_attributes=True) for c in codes],
                )
            )
        return result

    def create_group(self, group_key: str, group_name: str, description: str | None = None) -> CommonCodeGroupResponse:
        if self.repo.get_group_by_key(group_key):
            raise AppException(
                error_codes.VALIDATION_ERROR,
                f"그룹 키 '{group_key}'가 이미 존재합니다.",
                status.HTTP_409_CONFLICT,
            )
        group = self.repo.create_group(group_key, group_name, description)
        self.db.commit()
        return CommonCodeGroupResponse(
            id=group.id,
            group_key=group.group_key,
            group_name=group.group_name,
            description=group.description,
            codes=[],
        )

    def delete_group(self, group_key: str) -> None:
        group = self.repo.get_group_by_key(group_key)
        if not group:
            raise AppException(error_codes.RESOURCE_NOT_FOUND, f"그룹 '{group_key}'를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)
        self.repo.delete_group(group)
        self.db.commit()

    def add_code(
        self,
        group_key: str,
        code: str,
        label: str,
        sort_order: int = 0,
        meta_json: dict | None = None,
    ) -> CommonCodeResponse:
        group = self.repo.get_group_by_key(group_key)
        if not group:
            raise AppException(error_codes.RESOURCE_NOT_FOUND, f"그룹 '{group_key}'를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)
        common_code = self.repo.create_code(group.id, code, label, sort_order, meta_json)
        self.db.commit()
        return CommonCodeResponse.model_validate(common_code, from_attributes=True)

    def delete_code(self, code_id: int) -> None:
        code = self.repo.get_code(code_id)
        if not code:
            raise AppException(error_codes.RESOURCE_NOT_FOUND, "코드를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)
        self.repo.delete_code(code)
        self.db.commit()
