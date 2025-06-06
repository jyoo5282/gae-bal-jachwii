import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz

from ..app.main import app
from ..app.models.news import NewsSource, NewsArticle
from ..app.services.crawler_service import NewsCrawlerService

client = TestClient(app)

@pytest.fixture
def db(mocker):
    return mocker.Mock(spec=Session)

@pytest.fixture
def test_source():
    return NewsSource(
        id=1,
        name="테스트 소스",
        url="https://example.com",
        description="테스트용 뉴스 소스",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def test_article(test_source):
    return NewsArticle(
        id=1,
        source_id=test_source.id,
        source=test_source,
        title="테스트 기사",
        content="테스트 내용",
        url="https://example.com/1",
        published_at=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

def test_get_sources(mocker, db, test_source):
    """뉴스 소스 목록 조회 테스트"""
    db.query.return_value.all.return_value = [test_source]
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    response = client.get("/sources")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_source.name

def test_get_source(mocker, db, test_source):
    """특정 뉴스 소스 조회 테스트"""
    db.query.return_value.filter.return_value.first.return_value = test_source
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    response = client.get(f"/sources/{test_source.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == test_source.name

def test_get_source_not_found(mocker, db):
    """존재하지 않는 뉴스 소스 조회 테스트"""
    db.query.return_value.filter.return_value.first.return_value = None
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    response = client.get("/sources/999")
    assert response.status_code == 404

def test_get_articles(mocker, db, test_article):
    """뉴스 기사 목록 조회 테스트"""
    db.query.return_value.filter.return_value.order_by.return_value\
        .offset.return_value.limit.return_value.all.return_value = [test_article]
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    response = client.get("/articles")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_article.title

def test_get_articles_with_filters(mocker, db, test_article):
    """필터를 적용한 뉴스 기사 목록 조회 테스트"""
    db.query.return_value.filter.return_value.order_by.return_value\
        .offset.return_value.limit.return_value.all.return_value = [test_article]
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    params = {
        "source_id": test_article.source_id,
        "keyword": "테스트",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat()
    }
    response = client.get("/articles", params=params)
    assert response.status_code == 200

def test_get_today_articles(mocker, db, test_article):
    """오늘의 뉴스 기사 조회 테스트"""
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [test_article]
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    response = client.get("/today")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_article.title

def test_crawl_news(mocker, db):
    """뉴스 크롤링 테스트"""
    mock_crawler = mocker.Mock(spec=NewsCrawlerService)
    mock_crawler.crawl_all_sources.return_value = []
    mocker.patch("app.api.endpoints.news.NewsCrawlerService", return_value=mock_crawler)
    mocker.patch("app.api.endpoints.news.get_db", return_value=db)

    response = client.post("/crawl")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_articles" in data
    assert "new_articles" in data
    assert "sources" in data
    assert "errors" in data 