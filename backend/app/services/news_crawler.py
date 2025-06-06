from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import asyncio
from sqlalchemy.orm import Session
from ..models.news import NewsArticle, NewsSource

class NewsCrawler:
    def __init__(self, db: Session):
        self.db = db
        self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    async def crawl_all_sources(self):
        sources = self.db.query(NewsSource).all()
        total_articles = 0
        
        for source in sources:
            articles = await self.crawl_source(source)
            total_articles += len(articles)
            
        return total_articles

    async def crawl_source(self, source: NewsSource):
        try:
            self.driver.get(source.url)
            await asyncio.sleep(2)  # Wait for JavaScript to load
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            articles = []
            
            # 실제 크롤링 로직은 각 뉴스 사이트별로 다르게 구현해야 함
            # 여기서는 기본 구조만 구현
            
            for article in articles:
                self.save_article(article, source.id)
                
            return articles
            
        except Exception as e:
            print(f"Error crawling {source.name}: {str(e)}")
            return []

    def save_article(self, article_data: dict, source_id: int):
        existing = self.db.query(NewsArticle).filter_by(url=article_data["url"]).first()
        if existing:
            return
            
        article = NewsArticle(
            source_id=source_id,
            title=article_data["title"],
            content=article_data["content"],
            url=article_data["url"],
            author=article_data.get("author"),
            published_at=article_data.get("published_at"),
            keywords=article_data.get("keywords")
        )
        
        self.db.add(article)
        self.db.commit()

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit() 