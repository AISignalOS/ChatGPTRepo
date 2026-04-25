from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from database import get_db
from models import AnalyticsEvent, Tool
from schemas import AnalyticsResponse

router = APIRouter(tags=["analytics"])


@router.post("/api/tools/{tool_id}/click")
def track_click(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    db.execute(
        update(Tool).where(Tool.id == tool_id).values(click_count=Tool.click_count + 1)
    )
    event = AnalyticsEvent(tool_id=tool_id, event_type="click")
    db.add(event)
    db.commit()
    return {"status": "ok"}


@router.get("/api/analytics", response_model=list[AnalyticsResponse])
def get_analytics(limit: int = 10, db: Session = Depends(get_db)):
    tools = (
        db.query(Tool)
        .order_by(Tool.click_count.desc())
        .limit(limit)
        .all()
    )
    return [
        {"tool_id": t.id, "tool_name": t.name, "click_count": t.click_count}
        for t in tools
    ]
