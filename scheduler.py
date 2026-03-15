from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from config import DAILY_HOUR, DAILY_MINUTE, TIMEZONE
from handlers.daily import send_daily_digest
from rss_parser import fetch_all_news

async def scheduled_news_update():
    """Запланированное обновление RSS"""
    fetch_all_news()

async def scheduled_daily_digest():
    """Запланированная ежедневная рассылка"""
    await send_daily_digest()

def setup_scheduler():
    """Настраивает планировщик задач"""
    scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))
    
    # Обновление RSS каждые 6 часов
    scheduler.add_job(
        scheduled_news_update,
        trigger=CronTrigger(hour='*/6', minute=5),
        id='news_update'
    )
    
    # Ежедневная рассылка в 8:00
    scheduler.add_job(
        scheduled_daily_digest,
        trigger=CronTrigger(hour=DAILY_HOUR, minute=DAILY_MINUTE),
        id='daily_digest'
    )
    
    return scheduler