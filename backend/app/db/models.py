from sqlalchemy import String, Integer, DateTime, Text, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime, timezone
from typing import Optional, List

Base = declarative_base()

article_tag_association = Table(
    "article_tag_association",
    Base.metadata,
    Column("article_id", ForeignKey("curated_articles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    articles: Mapped[List["CuratedArticle"]] = relationship(
        "CuratedArticle",
        secondary=article_tag_association,
        back_populates="tags"
    )

class CuratedArticle(Base):
    __tablename__ = "curated_articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    author: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    url: Mapped[str] = mapped_column(Text)
    url_hash: Mapped[str] = mapped_column(String(64), unique=True)
    source: Mapped[str] = mapped_column(String(100))
    estimated_reading_time_min: Mapped[int] = mapped_column(Integer)
    reading_status: Mapped[str] = mapped_column(String(50), default="unread")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=article_tag_association,
        back_populates="articles",
        cascade="all"
    )

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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    article: Mapped["CuratedArticle"] = relationship(
        "CuratedArticle",
        back_populates="reflection"
    )
