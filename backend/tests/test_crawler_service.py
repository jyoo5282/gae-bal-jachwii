import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from ..app.services.crawler_service import NewsCrawlerService
from ..app.models.news import NewsSource, NewsArticle

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def mock_driver():
    with patch('selenium.webdriver.Chrome') as mock:
        yield mock

@pytest.fixture
def crawler_service(mock_db):
    service = NewsCrawlerService(mock_db)
    return service

def test_setup_driver(crawler_service, mock_driver):
    """WebDriver 설정 테스트"""
    crawler_service.setup_driver()
    assert crawler_service.driver is not None

def test_close_driver(crawler_service, mock_driver):
    """WebDriver 종료 테스트"""
    crawler_service.setup_driver()
    crawler_service.close_driver()
    assert crawler_service.driver is None

def test_get_today_articles(crawler_service, mock_db):
    """오늘 기사 수집 테스트"""
    source = NewsSource(
        id=1,
        name="매일경제",
        url="https://www.mk.co.kr/news/economy",
        description="매일경제 경제 뉴스"
    )
    
    with patch.object(crawler_service, '_crawl_maekyung') as mock_crawl:
        mock_crawl.return_value = [{
            "title": "테스트 기사",
            "content": "테스트 내용",
            "url": "https://example.com/1",
            "published_at": datetime.now()
        }]
        
        articles = crawler_service.get_today_articles(source)
        assert len(articles) == 1
        assert articles[0]["title"] == "테스트 기사"

def test_crawl_all_sources(crawler_service, mock_db):
    """전체 소스 크롤링 테스트"""
    sources = [
        NewsSource(
            id=1,
            name="매일경제",
            url="https://www.mk.co.kr/news/economy",
            description="매일경제 경제 뉴스"
        ),
        NewsSource(
            id=2,
            name="한국경제",
            url="https://www.hankyung.com/economy",
            description="한국경제 경제 뉴스"
        )
    ]
    
    mock_db.query.return_value.all.return_value = sources
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    with patch.object(crawler_service, 'get_today_articles') as mock_get:
        mock_get.return_value = [{
            "title": "테스트 기사",
            "content": "테스트 내용",
            "url": "https://example.com/1",
            "published_at": datetime.now()
        }]
        
        articles = crawler_service.crawl_all_sources()
        assert len(articles) == 2
        mock_db.commit.assert_called_once()

def test_duplicate_article_check(crawler_service, mock_db):
    """기사 중복 체크 테스트"""
    source = NewsSource(
        id=1,
        name="매일경제",
        url="https://www.mk.co.kr/news/economy",
        description="매일경제 경제 뉴스"
    )
    
    mock_db.query.return_value.all.return_value = [source]
    mock_db.query.return_value.filter_by.return_value.first.return_value = NewsArticle(
        id=1,
        source_id=1,
        title="중복 기사",
        content="중복 내용",
        url="https://example.com/1"
    )
    
    with patch.object(crawler_service, 'get_today_articles') as mock_get:
        mock_get.return_value = [{
            "title": "중복 기사",
            "content": "중복 내용",
            "url": "https://example.com/1",
            "published_at": datetime.now()
        }]
        
        articles = crawler_service.crawl_all_sources()
        assert len(articles) == 0  # 중복 기사는 추가되지 않아야 함 