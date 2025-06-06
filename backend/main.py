from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
import json

app = FastAPI(title="Economic News Aggregator")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 뉴스 소스 설정
NEWS_SOURCES = {
    'domestic': [
        {
            'name': '매일경제',
            'url': 'https://www.mk.co.kr/news/economy/',
            'article_selector': '.article_list > .news_node',
            'title_selector': 'h3.news_ttl',
            'link_selector': 'h3.news_ttl > a',
            'views_selector': '.view_count'
        },
        {
            'name': '네이버경제',
            'url': 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101',
            'article_selector': '#main_content .type06_headline > li',
            'title_selector': 'dt:not(.photo) > a',
            'link_selector': 'dt:not(.photo) > a',
            'views_selector': None
        },
        # ... 다른 국내 뉴스 소스들
    ],
    'international': [
        {
            'name': 'Reuters',
            'url': 'https://www.reuters.com/markets/',
            'article_selector': '.media-story-card',
            'title_selector': '.media-story-card__heading__eqhp9',
            'link_selector': 'a',
            'views_selector': None
        },
        # ... 다른 해외 뉴스 소스들
    ]
}

async def fetch_news(session, source):
    try:
        async with session.get(source['url']) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                articles = []
                
                for article in soup.select(source['article_selector'])[:5]:
                    title = article.select_one(source['title_selector'])
                    link = article.select_one(source['link_selector'])
                    views = None
                    
                    if source['views_selector']:
                        views_elem = article.select_one(source['views_selector'])
                        if views_elem:
                            views = views_elem.text.strip()
                    
                    if title and link:
                        articles.append({
                            'title': title.text.strip(),
                            'link': link.get('href'),
                            'views': views,
                            'source': source['name']
                        })
                
                return articles
            return []
    except Exception as e:
        print(f"Error fetching {source['name']}: {str(e)}")
        return []

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_path = Path("static/index.html")
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(), status_code=200)
    raise HTTPException(status_code=404, detail="index.html not found")

@app.get("/api/news")
async def get_news():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for category in NEWS_SOURCES.values():
            for source in category:
                tasks.append(fetch_news(session, source))
        
        results = await asyncio.gather(*tasks)
        
        news = {
            'domestic': [],
            'international': [],
            'timestamp': datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for i, category in enumerate(NEWS_SOURCES.keys()):
            start_idx = i * len(NEWS_SOURCES[category])
            end_idx = start_idx + len(NEWS_SOURCES[category])
            news[category] = [item for sublist in results[start_idx:end_idx] for item in sublist]
        
        return news

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 