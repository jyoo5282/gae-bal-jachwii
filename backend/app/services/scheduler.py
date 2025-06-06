import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from .crawler import NewsCrawler

logger = logging.getLogger(__name__)

class NewsScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.crawler = NewsCrawler()
        
    def start(self):
        """스케줄러 시작"""
        # 매일 오전 9시와 오후 6시에 크롤링 실행 (한국 시간)
        self.scheduler.add_job(
            self.crawler.crawl_all,
            CronTrigger(hour='9,18', timezone=timezone('Asia/Seoul')),
            id='crawl_news'
        )
        
        # 스케줄러 시작
        self.scheduler.start()
        logger.info("News scheduler started")
        
    def stop(self):
        """스케줄러 중지"""
        self.scheduler.shutdown()
        logger.info("News scheduler stopped")
        
    def run_now(self):
        """즉시 크롤링 실행"""
        logger.info("Running news crawler now")
        self.crawler.crawl_all() 