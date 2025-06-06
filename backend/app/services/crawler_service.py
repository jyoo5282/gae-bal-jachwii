from datetime import datetime, timedelta
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.news import NewsSource, NewsArticle
from ..core.config import settings

class NewsCrawlerService:
    def __init__(self, db: Session):
        self.db = db
        self.driver = None
        self.kst = pytz.timezone('Asia/Seoul')

    def setup_driver(self):
        """Selenium WebDriver 설정"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--lang=ko_KR")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def close_driver(self):
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_today_articles(self, source: NewsSource) -> List[dict]:
        """오늘 날짜의 기사만 수집"""
        articles = []
        today = datetime.now(self.kst).date()
        
        try:
            if source.name == "매일경제":
                articles = self._crawl_maekyung(today)
            elif source.name == "한국경제":
                articles = self._crawl_hankyung(today)
            elif source.name == "서울경제":
                articles = self._crawl_sedaily(today)
            elif source.name == "이데일리":
                articles = self._crawl_edaily(today)
            elif source.name == "머니투데이":
                articles = self._crawl_moneytoday(today)
        except Exception as e:
            print(f"Error crawling {source.name}: {str(e)}")
        
        return articles

    def _crawl_maekyung(self, target_date: datetime.date) -> List[dict]:
        """매일경제 크롤링"""
        articles = []
        self.driver.get("https://www.mk.co.kr/news/economy")
        
        try:
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news_item"))
            )

            for item in news_items[:10]:
                try:
                    date_text = item.find_element(By.CSS_SELECTOR, ".time").text
                    article_date = datetime.strptime(date_text, "%Y.%m.%d").date()
                    
                    if article_date == target_date:
                        title = item.find_element(By.CSS_SELECTOR, ".news_ttl").text
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        self.driver.get(link)
                        content = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".news_content"))
                        ).text
                        
                        articles.append({
                            "title": title,
                            "content": content,
                            "url": link,
                            "published_at": datetime.combine(article_date, datetime.min.time())
                        })
                except Exception as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error in MaeKyung crawler: {str(e)}")
        
        return articles

    def _crawl_hankyung(self, target_date: datetime.date) -> List[dict]:
        """한국경제 크롤링"""
        articles = []
        self.driver.get("https://www.hankyung.com/economy")
        
        try:
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article"))
            )

            for item in news_items[:10]:
                try:
                    date_text = item.find_element(By.CSS_SELECTOR, ".time").text
                    article_date = datetime.strptime(date_text, "%Y.%m.%d").date()
                    
                    if article_date == target_date:
                        title = item.find_element(By.CSS_SELECTOR, ".article-title").text
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        self.driver.get(link)
                        content = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".article-text"))
                        ).text
                        
                        articles.append({
                            "title": title,
                            "content": content,
                            "url": link,
                            "published_at": datetime.combine(article_date, datetime.min.time())
                        })
                except Exception as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error in HanKyung crawler: {str(e)}")
        
        return articles

    def _crawl_sedaily(self, target_date: datetime.date) -> List[dict]:
        """서울경제 크롤링"""
        articles = []
        self.driver.get("https://www.sedaily.com/NewsView/Economy")
        
        try:
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article"))
            )

            for item in news_items[:10]:
                try:
                    date_text = item.find_element(By.CSS_SELECTOR, ".date").text
                    article_date = datetime.strptime(date_text, "%Y-%m-%d").date()
                    
                    if article_date == target_date:
                        title = item.find_element(By.CSS_SELECTOR, ".article-title").text
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        self.driver.get(link)
                        content = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".article-body"))
                        ).text
                        
                        articles.append({
                            "title": title,
                            "content": content,
                            "url": link,
                            "published_at": datetime.combine(article_date, datetime.min.time())
                        })
                except Exception as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error in SeoulEconomy crawler: {str(e)}")
        
        return articles

    def _crawl_edaily(self, target_date: datetime.date) -> List[dict]:
        """이데일리 크롤링"""
        articles = []
        self.driver.get("https://www.edaily.co.kr/news/economy")
        
        try:
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news_list"))
            )

            for item in news_items[:10]:
                try:
                    date_text = item.find_element(By.CSS_SELECTOR, ".date").text
                    article_date = datetime.strptime(date_text, "%Y-%m-%d").date()
                    
                    if article_date == target_date:
                        title = item.find_element(By.CSS_SELECTOR, ".news_title").text
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        self.driver.get(link)
                        content = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".news_body"))
                        ).text
                        
                        articles.append({
                            "title": title,
                            "content": content,
                            "url": link,
                            "published_at": datetime.combine(article_date, datetime.min.time())
                        })
                except Exception as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error in EDaily crawler: {str(e)}")
        
        return articles

    def _crawl_moneytoday(self, target_date: datetime.date) -> List[dict]:
        """머니투데이 크롤링"""
        articles = []
        self.driver.get("https://news.mt.co.kr/mtmain.html?type=1")
        
        try:
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article_list"))
            )

            for item in news_items[:10]:
                try:
                    date_text = item.find_element(By.CSS_SELECTOR, ".date").text
                    article_date = datetime.strptime(date_text, "%Y-%m-%d").date()
                    
                    if article_date == target_date:
                        title = item.find_element(By.CSS_SELECTOR, ".article_title").text
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        self.driver.get(link)
                        content = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".article_content"))
                        ).text
                        
                        articles.append({
                            "title": title,
                            "content": content,
                            "url": link,
                            "published_at": datetime.combine(article_date, datetime.min.time())
                        })
                except Exception as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error in MoneyToday crawler: {str(e)}")
        
        return articles

    def crawl_all_sources(self) -> List[NewsArticle]:
        """모든 뉴스 소스에서 오늘 기사 수집"""
        if not self.driver:
            self.setup_driver()

        all_articles = []
        sources = self.db.query(NewsSource).all()

        for source in sources:
            try:
                articles = self.get_today_articles(source)
                
                for article_data in articles:
                    # 중복 체크
                    existing = self.db.query(NewsArticle).filter_by(url=article_data["url"]).first()
                    if not existing:
                        article = NewsArticle(
                            source_id=source.id,
                            **article_data
                        )
                        self.db.add(article)
                        all_articles.append(article)
                
            except Exception as e:
                print(f"Error crawling source {source.name}: {str(e)}")
                continue

        self.db.commit()
        return all_articles

    def __del__(self):
        self.close_driver() 