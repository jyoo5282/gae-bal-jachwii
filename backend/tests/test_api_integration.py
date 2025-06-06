import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime

from ..app.main import app
from ..app.db.session import get_db
from ..app.models.news import NewsSource, NewsArticle
from ..app.core.init_db import init_news_sources

client = TestClient(app)

def test_get_sources():
    """뉴스 소스 목록 조회 테스트"""
    response = client.get("/sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) > 0
    assert all(isinstance(source["name"], str) for source in sources)

def test_get_articles():
    """뉴스 기사 목록 조회 테스트"""
    response = client.get("/articles")
    assert response.status_code == 200
    articles = response.json()
    assert isinstance(articles, list)
    if len(articles) > 0:
        assert all(isinstance(article["title"], str) for article in articles)
        assert all(isinstance(article["content"], str) for article in articles)
        assert all(isinstance(article["url"], str) for article in articles)

def test_crawl_news():
    """뉴스 크롤링 테스트"""
    response = client.post("/crawl")
    assert response.status_code == 200
    articles = response.json()
    assert isinstance(articles, list)
    if len(articles) > 0:
        assert all(isinstance(article["title"], str) for article in articles)
        assert all(isinstance(article["content"], str) for article in articles)
        assert all(isinstance(article["url"], str) for article in articles)

def test_filter_articles():
    """뉴스 기사 필터링 테스트"""
    # 소스별 필터링
    response = client.get("/articles?source=매일경제")
    assert response.status_code == 200
    articles = response.json()
    if len(articles) > 0:
        assert all(article["source"]["name"] == "매일경제" for article in articles)

    # 날짜별 필터링
    today = datetime.now().strftime("%Y-%m-%d")
    response = client.get(f"/articles?date={today}")
    assert response.status_code == 200
    articles = response.json()
    if len(articles) > 0:
        assert all(article["published_at"].startswith(today) for article in articles)

def test_error_handling():
    """에러 처리 테스트"""
    # 잘못된 소스 ID
    response = client.get("/sources/999999")
    assert response.status_code == 404

    # 잘못된 기사 ID
    response = client.get("/articles/999999")
    assert response.status_code == 404

    # 잘못된 날짜 형식
    response = client.get("/articles?date=invalid-date")
    assert response.status_code == 400 