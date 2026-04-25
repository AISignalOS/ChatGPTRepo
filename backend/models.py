from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base


class Tool(Base):
    __tablename__ = "tools"

    id               = Column(Integer, primary_key=True, index=True)
    name             = Column(String(255), nullable=False)
    url              = Column(String(1024), unique=True, nullable=False, index=True)
    description      = Column(Text)
    raw_content      = Column(Text)
    signal_summary   = Column(Text)
    use_cases        = Column(Text)   # JSON array stored as string
    price_tier       = Column(String(50))  # free | freemium | paid | enterprise
    target_audience  = Column(Text)
    created_at       = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    click_count      = Column(Integer, default=0)
    view_count       = Column(Integer, default=0)


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id             = Column(Integer, primary_key=True, index=True)
    tool_id        = Column(Integer, ForeignKey("tools.id"), nullable=False)
    event_type     = Column(String(50))   # "click" | "view"
    timestamp      = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # Renamed from `metadata` — that name is reserved by SQLAlchemy's DeclarativeBase.
    event_metadata = Column("metadata", Text)  # JSON blob
