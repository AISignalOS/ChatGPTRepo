import json
from typing import Optional
from pydantic import BaseModel, field_validator


class ToolCreate(BaseModel):
    name: str
    url: str
    description: Optional[str] = None
    raw_content: str


class ToolResponse(BaseModel):
    id: int
    name: str
    url: str
    description: Optional[str] = None
    signal_summary: Optional[str] = None
    use_cases: list[str] = []
    price_tier: Optional[str] = None
    target_audience: Optional[str] = None
    click_count: int = 0
    view_count: int = 0
    created_at: str = ""

    @field_validator("use_cases", mode="before")
    @classmethod
    def parse_use_cases(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, ValueError):
                return []
        return v or []

    @field_validator("created_at", mode="before")
    @classmethod
    def format_created_at(cls, v):
        if v is None:
            return ""
        return str(v)

    model_config = {"from_attributes": True}


class AnalyticsResponse(BaseModel):
    tool_id: int
    tool_name: str
    click_count: int
