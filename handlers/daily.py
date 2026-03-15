from telegram import Bot
from database import get_active_users, get_news_cache
from config import BOT_TOKEN, RUBRICS
import asyncio
from datetime import datetime

async def send_daily_digest():
    """Отправляет дайджест всем активным подписчикам"""
    print(f"[{datetime.now()}] Начинаю ежедневную рассылку...")
    
    bot = Bot(token=BOT_TOKEN)
    users = get_active_users()
    
    for user in users:
        if not user['rubrics']:
            continue
        
        # Собираем новости по выбранным рубрикам
        digest = f"📰 *Ваш дайджест на {datetime.now().strftime('%d.%m.%Y')}*\n\n"
        
        for rubric_callback in user['rubrics']:
            # Находим название рубрики
            rubric_name = next((r["name"] for r in RUBRICS if r["callback"] == rubric_callback), rubric_callback)
            
            # Получаем новости из кэша
            news = get_news_cache(rubric_callback)
            
            if news:
                digest += f"*{rubric_name}*\n"
                for i, item in enumerate(news, 1):
                    digest += f"{i}. [{item['title']}]({item['link']})\n"
                digest += "\n"
            else:
                digest += f"*{rubric_name}*\n_Нет свежих новостей_\n\n"
        
        digest += "\n✨ Чтобы изменить рубрики, отправьте /start"
        
        try:
            await bot.send_message(
                chat_id=user['chat_id'],
                text=digest,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            print(f"  → Отправлено пользователю {user['user_id']}")
            await asyncio.sleep(1)  # Задержка между сообщениями
        except Exception as e:
            print(f"  → Ошибка при отправке пользователю {user['user_id']}: {e}")
    
    print(f"[{datetime.now()}] Рассылка завершена")