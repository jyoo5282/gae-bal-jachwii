from sqlalchemy.orm import Session
from ..models.news import NewsSource

def init_news_sources(db: Session):
    sources = [
        {
            "name": "매일경제",
            "url": "https://www.mk.co.kr/news/economy",
            "description": "매일경제 경제 뉴스"
        },
        {
            "name": "한국경제",
            "url": "https://www.hankyung.com/economy",
            "description": "한국경제 경제 뉴스"
        },
        {
            "name": "서울경제",
            "url": "https://www.sedaily.com/NewsView/Economy",
            "description": "서울경제 경제 뉴스"
        },
        {
            "name": "이데일리",
            "url": "https://www.edaily.co.kr/news/economy",
            "description": "이데일리 경제 뉴스"
        },
        {
            "name": "머니투데이",
            "url": "https://news.mt.co.kr/mtmain.html?type=1",
            "description": "머니투데이 경제 뉴스"
        }
    ]

    for source_data in sources:
        existing = db.query(NewsSource).filter_by(name=source_data["name"]).first()
        if not existing:
            source = NewsSource(**source_data)
            db.add(source)
    
    db.commit() 