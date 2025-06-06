import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def fetch_korean_economy_news():
    # 오늘 날짜 구하기 (KST 기준)
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).strftime('%Y%m%d')
    
    # 네이버 경제 뉴스 리스트 URL
    url = f"https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=101&date={today}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()  # 에러 발생시 예외 발생
        
        soup = BeautifulSoup(res.text, 'html.parser')
        news_items = soup.select('.newsflash_body .type06_headline li dl, .newsflash_body .type06 li dl')
        
        news_list = []
        for item in news_items:
            title_tag = item.select_one('dt:not(.photo) a, dt:last-child a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']
                news_list.append((title, link))
        return news_list
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

if __name__ == "__main__":
    news = fetch_korean_economy_news()
    print("오늘의 한국 경제 뉴스")
    print("="*30)
    for i, (title, link) in enumerate(news, 1):
        print(f"{i}. {title}\n   {link}\n") 