from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..models.news import NewsArticle, NewsSource
from ..services.scheduler import NewsScheduler

router = APIRouter()
scheduler = NewsScheduler()

@router.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 스케줄러 시작"""
    scheduler.start()

@router.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 스케줄러 중지"""
    scheduler.stop()

@router.get("/news", response_model=List[dict])
async def get_news(db: Session = Depends(get_db)):
    """최신 뉴스 기사 목록 조회"""
    articles = db.query(NewsArticle).order_by(NewsArticle.published_at.desc()).all()
    return [
        {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "url": article.url,
            "source_name": article.source.name,
            "published_at": article.published_at.isoformat()
        }
        for article in articles
    ]

@router.get("/sources", response_model=List[dict])
async def get_sources(db: Session = Depends(get_db)):
    """뉴스 소스 목록 조회"""
    sources = db.query(NewsSource).all()
    return [
        {
            "id": source.id,
            "name": source.name,
            "url": source.url,
            "is_active": source.is_active
        }
        for source in sources
    ]

@router.post("/crawl")
async def trigger_crawl():
    """수동으로 크롤링 실행"""
    try:
        scheduler.run_now()
        return {"message": "Crawling started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 