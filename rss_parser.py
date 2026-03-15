import feedparser
import hashlib
import json
import os
from datetime import datetime, timedelta
from config import RUBRICS
from database import save_news_cache

def fetch_rss_news(rubric_callback, rss_url, limit=3):
    """Получает последние новости из RSS-ленты"""
    try:
        feed = feedparser.parse(rss_url)
        news = []
        
        for entry in feed.entries[:limit]:
            news.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'summary': entry.get('summary', '')[:200] + '...' if entry.get('summary') else ''
            })
        
        # Сохраняем в кэш
        save_news_cache(rubric_callback, news)
        
        return news
    except Exception as e:
        print(f"Ошибка при парсинге RSS {rss_url}: {e}")
        return []

def fetch_all_news():
    """Обновляет все RSS-ленты"""
    print(f"[{datetime.now()}] Начинаю обновление всех RSS-лент...")
    
    for rubric in RUBRICS:
        print(f"  → Обновляю {rubric['name']}...")
        fetch_rss_news(rubric['callback'], rubric['rss'])
    
    print(f"[{datetime.now()}] Обновление завершено")

def get_news_for_rubrics(rubrics):
    """Собирает новости для списка рубрик"""
    result = []
    
    for rubric_callback in rubrics:
        news = get_news_cache(rubric_callback)
        if news:
            # Находим название рубрики
            rubric_name = next((r["name"] for r in RUBRICS if r["callback"] == rubric_callback), rubric_callback)
            result.append({
                'rubric': rubric_name,
                'rubric_callback': rubric_callback,
                'news': news
            })
    
    return result