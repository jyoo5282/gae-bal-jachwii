from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .base import Base, TimeStampMixin

class NewsSource(Base, TimeStampMixin):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

class NewsArticle(Base, TimeStampMixin):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    author = Column(String(100), nullable=True)
    published_at = Column(String(50), nullable=True)
    keywords = Column(String(500), nullable=True) 