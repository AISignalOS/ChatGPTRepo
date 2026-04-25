import json
from urllib.parse import urlparse, urlunparse
from sqlalchemy.orm import Session
from models import Tool
from schemas import ToolCreate


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        "",
        "",
        "",
    ))
    return normalized


def upsert_tool(db: Session, payload: ToolCreate, summary_data: dict, existing: Tool | None) -> Tool:
    use_cases_json = json.dumps(summary_data.get("use_cases", []))

    if existing:
        existing.name            = payload.name
        existing.description     = payload.description
        existing.raw_content     = payload.raw_content
        existing.signal_summary  = summary_data.get("signal_summary")
        existing.use_cases       = use_cases_json
        existing.price_tier      = summary_data.get("price_tier")
        existing.target_audience = summary_data.get("target_audience")
        db.commit()
        db.refresh(existing)
        return existing

    tool = Tool(
        name            = payload.name,
        url             = normalize_url(payload.url),
        description     = payload.description,
        raw_content     = payload.raw_content,
        signal_summary  = summary_data.get("signal_summary"),
        use_cases       = use_cases_json,
        price_tier      = summary_data.get("price_tier"),
        target_audience = summary_data.get("target_audience"),
    )
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool
