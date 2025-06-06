from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import re
from typing import List, Dict, Any

class NewsCrawler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def clean_text(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

class MaeKyungCrawler(NewsCrawler):
    def crawl(self) -> List[Dict[str, Any]]:
        articles = []
        try:
            # 경제 뉴스 목록 페이지로 이동
            self.driver.get("https://www.mk.co.kr/news/economy")
            
            # 뉴스 항목들 찾기
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news_item"))
            )

            for item in news_items[:10]:  # 상위 10개 기사만 수집
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".news_ttl").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    # 상세 페이지로 이동
                    self.driver.get(link)
                    
                    content = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".news_content"))
                    ).text
                    
                    articles.append({
                        "title": self.clean_text(title),
                        "content": self.clean_text(content),
                        "url": link,
                        "published_at": datetime.now()  # 실제로는 기사에서 날짜 추출 필요
                    })
                    
                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in MaeKyung crawler: {str(e)}")
            
        return articles

class HanKyungCrawler(NewsCrawler):
    def crawl(self) -> List[Dict[str, Any]]:
        articles = []
        try:
            self.driver.get("https://www.hankyung.com/economy")
            
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".article-title").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    self.driver.get(link)
                    
                    content = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".article-text"))
                    ).text
                    
                    articles.append({
                        "title": self.clean_text(title),
                        "content": self.clean_text(content),
                        "url": link,
                        "published_at": datetime.now()
                    })
                    
                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in HanKyung crawler: {str(e)}")
            
        return articles

class SeoulEconomyCrawler(NewsCrawler):
    def crawl(self) -> List[Dict[str, Any]]:
        articles = []
        try:
            self.driver.get("https://www.sedaily.com/NewsView/Economy")
            
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".article-title").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    self.driver.get(link)
                    
                    content = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".article-body"))
                    ).text
                    
                    articles.append({
                        "title": self.clean_text(title),
                        "content": self.clean_text(content),
                        "url": link,
                        "published_at": datetime.now()
                    })
                    
                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in SeoulEconomy crawler: {str(e)}")
            
        return articles

class EDailyCrawler(NewsCrawler):
    def crawl(self) -> List[Dict[str, Any]]:
        articles = []
        try:
            self.driver.get("https://www.edaily.co.kr/news/economy")
            
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news_list"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".news_title").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    self.driver.get(link)
                    
                    content = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".news_body"))
                    ).text
                    
                    articles.append({
                        "title": self.clean_text(title),
                        "content": self.clean_text(content),
                        "url": link,
                        "published_at": datetime.now()
                    })
                    
                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in EDaily crawler: {str(e)}")
            
        return articles

class MoneyTodayCrawler(NewsCrawler):
    def crawl(self) -> List[Dict[str, Any]]:
        articles = []
        try:
            self.driver.get("https://news.mt.co.kr/mtmain.html?type=1")
            
            news_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article_list"))
            )

            for item in news_items[:10]:
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".article_title").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    self.driver.get(link)
                    
                    content = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".article_content"))
                    ).text
                    
                    articles.append({
                        "title": self.clean_text(title),
                        "content": self.clean_text(content),
                        "url": link,
                        "published_at": datetime.now()
                    })
                    
                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Error crawling article: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in MoneyToday crawler: {str(e)}")
            
        return articles

def get_crawler_for_source(source_name: str, driver: webdriver.Chrome) -> NewsCrawler:
    crawlers = {
        "매일경제": MaeKyungCrawler,
        "한국경제": HanKyungCrawler,
        "서울경제": SeoulEconomyCrawler,
        "이데일리": EDailyCrawler,
        "머니투데이": MoneyTodayCrawler
    }
    
    crawler_class = crawlers.get(source_name)
    if not crawler_class:
        raise ValueError(f"No crawler found for source: {source_name}")
        
    return crawler_class(driver) 