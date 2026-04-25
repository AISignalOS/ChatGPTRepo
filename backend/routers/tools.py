from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Tool
from schemas import ToolCreate, ToolResponse
from services.claude_service import generate_signal_summary
from services.tool_service import normalize_url, upsert_tool

router = APIRouter(prefix="/api/tools", tags=["tools"])


@router.post("/", response_model=ToolResponse, status_code=201)
def create_tool(payload: ToolCreate, db: Session = Depends(get_db)):
    normalized = normalize_url(payload.url)
    existing = db.query(Tool).filter(Tool.url == normalized).first()

    summary_data = generate_signal_summary(
        raw_content=payload.raw_content,
        tool_name=payload.name,
        tool_url=payload.url,
    )

    tool = upsert_tool(db, payload, summary_data, existing)
    return tool


@router.get("/", response_model=list[ToolResponse])
def list_tools(
    use_case: str = Query(None),
    price_tier: str = Query(None),
    search: str = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(Tool)

    if price_tier:
        q = q.filter(Tool.price_tier == price_tier)
    if use_case:
        q = q.filter(Tool.use_cases.like(f'%"{use_case}"%'))
    if search:
        q = q.filter(
            Tool.name.ilike(f"%{search}%") | Tool.signal_summary.ilike(f"%{search}%")
        )

    return q.order_by(Tool.click_count.desc()).limit(limit).all()


@router.get("/{tool_id}", response_model=ToolResponse)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    tool.view_count += 1
    db.commit()
    db.refresh(tool)
    return tool
