#!/usr/bin/env python3
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from database import init_database
from handlers.start import start_command
from handlers.callback import handle_callback
from scheduler import setup_scheduler
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application: Application):
    """Действия после инициализации бота"""
    # Устанавливаем команды бота
    await application.bot.set_my_commands([
        ("start", "Начать работу с ботом"),
    ])
    logger.info("Бот запущен!")

def main():
    """Главная функция"""
    # Инициализируем базу данных
    init_database()
    logger.info("База данных инициализирована")
    
    # Создаём приложение
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Настраиваем планировщик
    scheduler = setup_scheduler()
    scheduler.start()
    logger.info("Планировщик задач запущен")
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()