from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ...db.session import get_db
from ...services.crawler_service import CrawlerService
from ...schemas.news import NewsArticle

router = APIRouter()

@router.post("/crawl", response_model=List[NewsArticle])
def crawl_news(db: Session = Depends(get_db)):
    """
    모든 뉴스 소스에서 최신 기사를 크롤링합니다.
    """
    crawler_service = CrawlerService(db)
    articles = crawler_service.crawl_all_sources()
    return articles 