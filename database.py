import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

def init_database():
    """Создаёт таблицы, если их нет"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            username TEXT,
            rubrics TEXT,  -- JSON массив выбранных рубрик
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_sent_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Таблица кэша новостей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_cache (
            rubric TEXT PRIMARY KEY,
            news_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Получает данные пользователя по ID"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_user(user_id, chat_id, username, rubrics):
    """Сохраняет или обновляет пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    rubrics_json = json.dumps(rubrics)
    
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, chat_id, username, rubrics, subscribed_at, is_active)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 1)
    ''', (user_id, chat_id, username, rubrics_json))
    
    conn.commit()
    conn.close()

def update_user_rubrics(user_id, rubrics):
    """Обновляет выбранные рубрики пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    rubrics_json = json.dumps(rubrics)
    
    cursor.execute('''
        UPDATE users SET rubrics = ? WHERE user_id = ?
    ''', (rubrics_json, user_id))
    
    conn.commit()
    conn.close()

def unsubscribe_user(user_id):
    """Отписывает пользователя (деактивирует)"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET is_active = 0 WHERE user_id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def get_active_users():
    """Получает всех активных подписчиков"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, chat_id, rubrics FROM users WHERE is_active = 1")
    users = cursor.fetchall()
    conn.close()
    
    result = []
    for user in users:
        result.append({
            'user_id': user[0],
            'chat_id': user[1],
            'rubrics': json.loads(user[2]) if user[2] else []
        })
    return result

def save_news_cache(rubric, news):
    """Сохраняет последние новости по рубрике"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    news_json = json.dumps(news)
    
    cursor.execute('''
        INSERT OR REPLACE INTO news_cache (rubric, news_json, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (rubric, news_json))
    
    conn.commit()
    conn.close()

def get_news_cache(rubric):
    """Получает последние новости по рубрике"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT news_json FROM news_cache WHERE rubric = ?", (rubric,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0])
    return []