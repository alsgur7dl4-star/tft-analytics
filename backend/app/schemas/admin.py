from datetime import datetime
from typing import Any

from pydantic import BaseModel


class JobRunResponse(BaseModel):
    id: int
    job_name: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    message: str | None = None
    meta_json: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class JobTriggerResponse(BaseModel):
    job_run_id: int
    status: str
    message: str


class BatchJobLogResponse(BaseModel):
    id: int
    job_run_id: int
    log_level: str
    step: str | None = None
    message: str
    meta_json: dict[str, Any] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class DataSourceResponse(BaseModel):
    id: int
    source_key: str
    source_name: str
    status: str
    meta_json: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class CommonCodeResponse(BaseModel):
    id: int
    code: str
    label: str
    sort_order: int
    meta_json: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class CommonCodeGroupResponse(BaseModel):
    id: int
    group_key: str
    group_name: str
    description: str | None = None
    codes: list[CommonCodeResponse] = []


class CommonCodeGroupCreate(BaseModel):
    group_key: str
    group_name: str
    description: str | None = None


class CommonCodeCreate(BaseModel):
    code: str
    label: str
    sort_order: int = 0
    meta_json: dict[str, Any] | None = None
