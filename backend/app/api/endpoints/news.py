from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import pytz

from ...db.session import get_db
from ...services.crawler_service import NewsCrawlerService
from ...models.news import NewsSource, NewsArticle
from ...schemas.news import (
    NewsSource as NewsSourceSchema,
    NewsArticle as NewsArticleSchema,
    NewsFilter,
    NewsCrawlResponse
)

router = APIRouter()

@router.get("/sources", response_model=List[NewsSourceSchema])
def get_sources(db: Session = Depends(get_db)):
    """뉴스 소스 목록 조회"""
    return db.query(NewsSource).all()

@router.get("/sources/{source_id}", response_model=NewsSourceSchema)
def get_source(source_id: int, db: Session = Depends(get_db)):
    """특정 뉴스 소스 조회"""
    source = db.query(NewsSource).filter(NewsSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="News source not found")
    return source

@router.get("/articles", response_model=List[NewsArticleSchema])
def get_articles(
    source_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    keyword: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """뉴스 기사 목록 조회"""
    query = db.query(NewsArticle)

    if source_id:
        query = query.filter(NewsArticle.source_id == source_id)
    
    if start_date:
        query = query.filter(NewsArticle.published_at >= start_date)
    
    if end_date:
        query = query.filter(NewsArticle.published_at <= end_date)
    
    if keyword:
        query = query.filter(
            NewsArticle.title.ilike(f"%{keyword}%") |
            NewsArticle.content.ilike(f"%{keyword}%")
        )
    
    query = query.order_by(NewsArticle.published_at.desc())
    return query.offset(skip).limit(limit).all()

@router.get("/articles/{article_id}", response_model=NewsArticleSchema)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """특정 뉴스 기사 조회"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return article

@router.post("/crawl", response_model=NewsCrawlResponse)
def crawl_news(db: Session = Depends(get_db)):
    """뉴스 크롤링 실행"""
    crawler = NewsCrawlerService(db)
    errors = []
    sources = []
    total_articles = 0
    new_articles = 0

    try:
        articles = crawler.crawl_all_sources()
        
        # 결과 집계
        sources = list(set(article.source.name for article in articles))
        total_articles = len(articles)
        new_articles = sum(1 for article in articles if article.id is None)

    except Exception as e:
        errors.append(str(e))
    finally:
        crawler.close_driver()

    return NewsCrawlResponse(
        total_articles=total_articles,
        new_articles=new_articles,
        sources=sources,
        errors=errors
    )

@router.get("/today", response_model=List[NewsArticleSchema])
def get_today_articles(
    source_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """오늘 수집된 뉴스 기사 조회"""
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).date()
    start_datetime = datetime.combine(today, datetime.min.time())
    end_datetime = datetime.combine(today, datetime.max.time())

    query = db.query(NewsArticle).filter(
        NewsArticle.published_at >= start_datetime,
        NewsArticle.published_at <= end_datetime
    )

    if source_id:
        query = query.filter(NewsArticle.source_id == source_id)

    return query.order_by(NewsArticle.published_at.desc()).all() 