from datetime import datetime
import logging
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from ..models.news import NewsArticle, NewsSource
from ..db.database import SessionLocal

logger = logging.getLogger(__name__)

class NewsCrawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # GUI 없이 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def crawl_maeil(self, source: NewsSource) -> List[NewsArticle]:
        """매일경제 뉴스 크롤링"""
        articles = []
        try:
            self.driver.get(source.url)
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list_block"))
            )

            for item in news_items[:10]:  # 최근 10개 기사만 수집
                try:
                    title = item.find_element(By.CSS_SELECTOR, "dt.tit > a").text
                    url = item.find_element(By.CSS_SELECTOR, "dt.tit > a").get_attribute("href")
                    content = item.find_element(By.CSS_SELECTOR, "dd.txt").text
                    date_str = item.find_element(By.CSS_SELECTOR, "dd.date").text
                    
                    # 날짜 파싱
                    date = datetime.strptime(date_str, "%Y.%m.%d %H:%M")
                    
                    articles.append(NewsArticle(
                        title=title,
                        content=content,
                        url=url,
                        source_id=source.id,
                        published_at=date
                    ))
                except (NoSuchElementException, ValueError) as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
                    
        except TimeoutException:
            logger.error("Timeout while crawling Maeil Business News")
        except Exception as e:
            logger.error(f"Error crawling Maeil Business News: {str(e)}")
            
        return articles

    def crawl_hankyung(self, source: NewsSource) -> List[NewsArticle]:
        """한국경제 뉴스 크롤링"""
        articles = []
        try:
            self.driver.get(source.url)
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news-list > li"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "h3.news-tit > a").text
                    url = item.find_element(By.CSS_SELECTOR, "h3.news-tit > a").get_attribute("href")
                    content = item.find_element(By.CSS_SELECTOR, "p.news-dsc").text
                    date_str = item.find_element(By.CSS_SELECTOR, "span.time").text
                    
                    # 날짜 파싱
                    date = datetime.strptime(date_str, "%Y.%m.%d %H:%M")
                    
                    articles.append(NewsArticle(
                        title=title,
                        content=content,
                        url=url,
                        source_id=source.id,
                        published_at=date
                    ))
                except (NoSuchElementException, ValueError) as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
                    
        except TimeoutException:
            logger.error("Timeout while crawling Hankyung News")
        except Exception as e:
            logger.error(f"Error crawling Hankyung News: {str(e)}")
            
        return articles

    def crawl_sedaily(self, source: NewsSource) -> List[NewsArticle]:
        """서울경제 뉴스 크롤링"""
        articles = []
        try:
            self.driver.get(source.url)
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news_list > li"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "h2 > a").text
                    url = item.find_element(By.CSS_SELECTOR, "h2 > a").get_attribute("href")
                    content = item.find_element(By.CSS_SELECTOR, "p.con").text
                    date_str = item.find_element(By.CSS_SELECTOR, "span.date").text
                    
                    # 날짜 파싱
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    
                    articles.append(NewsArticle(
                        title=title,
                        content=content,
                        url=url,
                        source_id=source.id,
                        published_at=date
                    ))
                except (NoSuchElementException, ValueError) as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
                    
        except TimeoutException:
            logger.error("Timeout while crawling Seoul Economic Daily")
        except Exception as e:
            logger.error(f"Error crawling Seoul Economic Daily: {str(e)}")
            
        return articles

    def crawl_edaily(self, source: NewsSource) -> List[NewsArticle]:
        """이데일리 뉴스 크롤링"""
        articles = []
        try:
            self.driver.get(source.url)
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news_list > li"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "a.news_tit").text
                    url = item.find_element(By.CSS_SELECTOR, "a.news_tit").get_attribute("href")
                    content = item.find_element(By.CSS_SELECTOR, "p.news_dsc").text
                    date_str = item.find_element(By.CSS_SELECTOR, "span.date").text
                    
                    # 날짜 파싱
                    date = datetime.strptime(date_str, "%Y.%m.%d %H:%M")
                    
                    articles.append(NewsArticle(
                        title=title,
                        content=content,
                        url=url,
                        source_id=source.id,
                        published_at=date
                    ))
                except (NoSuchElementException, ValueError) as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
                    
        except TimeoutException:
            logger.error("Timeout while crawling eDaily News")
        except Exception as e:
            logger.error(f"Error crawling eDaily News: {str(e)}")
            
        return articles

    def crawl_mt(self, source: NewsSource) -> List[NewsArticle]:
        """머니투데이 뉴스 크롤링"""
        articles = []
        try:
            self.driver.get(source.url)
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list_block"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "strong.title > a").text
                    url = item.find_element(By.CSS_SELECTOR, "strong.title > a").get_attribute("href")
                    content = item.find_element(By.CSS_SELECTOR, "p.text").text
                    date_str = item.find_element(By.CSS_SELECTOR, "span.time").text
                    
                    # 날짜 파싱
                    date = datetime.strptime(date_str, "%Y.%m.%d %H:%M")
                    
                    articles.append(NewsArticle(
                        title=title,
                        content=content,
                        url=url,
                        source_id=source.id,
                        published_at=date
                    ))
                except (NoSuchElementException, ValueError) as e:
                    logger.error(f"Error parsing article: {str(e)}")
                    continue
                    
        except TimeoutException:
            logger.error("Timeout while crawling Money Today News")
        except Exception as e:
            logger.error(f"Error crawling Money Today News: {str(e)}")
            
        return articles

    def crawl_all(self) -> None:
        """모든 뉴스 소스에서 기사 크롤링"""
        db = SessionLocal()
        try:
            sources = db.query(NewsSource).filter(NewsSource.is_active == True).all()
            
            for source in sources:
                articles = []
                if "mk.co.kr" in source.url:
                    articles = self.crawl_maeil(source)
                elif "hankyung.com" in source.url:
                    articles = self.crawl_hankyung(source)
                elif "sedaily.com" in source.url:
                    articles = self.crawl_sedaily(source)
                elif "edaily.co.kr" in source.url:
                    articles = self.crawl_edaily(source)
                elif "mt.co.kr" in source.url:
                    articles = self.crawl_mt(source)
                
                # 새로운 기사만 저장
                for article in articles:
                    existing = db.query(NewsArticle).filter(
                        NewsArticle.url == article.url
                    ).first()
                    
                    if not existing:
                        db.add(article)
                
                db.commit()
                
        except Exception as e:
            logger.error(f"Error in crawl_all: {str(e)}")
            db.rollback()
        finally:
            db.close() 