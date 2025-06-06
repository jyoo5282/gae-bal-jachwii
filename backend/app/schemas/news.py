from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NewsSourceBase(BaseModel):
    name: str
    url: str
    description: Optional[str] = None

class NewsSourceCreate(NewsSourceBase):
    pass

class NewsSource(NewsSourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NewsArticleBase(BaseModel):
    title: str
    content: str
    url: str
    published_at: datetime

class NewsArticleCreate(NewsArticleBase):
    source_id: int

class NewsArticle(NewsArticleBase):
    id: int
    source_id: int
    source: NewsSource
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NewsFilter(BaseModel):
    source_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    keyword: Optional[str] = None

class NewsCrawlResponse(BaseModel):
    total_articles: int
    new_articles: int
    sources: List[str]
    errors: List[str] 