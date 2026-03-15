from telegram import Update
from telegram.ext import ContextTypes
from database import get_user
from keyboards import get_rubrics_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Проверяем, есть ли пользователь в базе
    existing_user = get_user(user.id)
    
    if existing_user:
        # Пользователь уже есть - показываем его текущие рубрики
        await update.message.reply_text(
            f"С возвращением, {user.first_name}! 👋\n\n"
            "Выберите рубрики (можно изменить выбор).",
            reply_markup=get_rubrics_keyboard()
        )
    else:
        # Новый пользователь
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n\n"
            "Я бот новостных дайджестов.\n"
            "Выберите от 1 до 5 интересующих рубрик:",
            reply_markup=get_rubrics_keyboard()
        )
    
    # Сохраняем состояние выбора в контексте
    context.user_data['selected_rubrics'] = []