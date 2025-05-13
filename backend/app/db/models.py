from sqlalchemy import String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from typing import Optional

Base = declarative_base()

class CuratedArticle(Base):
    __tablename__ = "curated_articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    author: Mapped[str] = mapped_column(String(256), nullable=True)
    url: Mapped[str] = mapped_column(Text)
    url_hash: Mapped[str] = mapped_column(String(64), unique=True)
    source: Mapped[str] = mapped_column(String(100))
    tags: Mapped[str] = mapped_column(String(512))
    estimated_reading_time_min: Mapped[int] = mapped_column(Integer)
    reading_status: Mapped[str] = mapped_column(String(50), default="unread")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    reflection: Mapped[Optional["Reflection"]] = relationship(
        "Reflection",
        back_populates="article",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Reflection(Base):
    __tablename__ = "reflections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("curated_articles.id"), unique=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    article: Mapped["CuratedArticle"] = relationship("CuratedArticle", back_populates="reflection")