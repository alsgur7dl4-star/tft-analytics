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


class DataSourceResponse(BaseModel):
    id: int
    source_key: str
    source_name: str
    status: str
    meta_json: dict[str, Any] | None = None

    model_config = {"from_attributes": True}

