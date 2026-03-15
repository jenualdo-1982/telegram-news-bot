from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import RUBRICS

def get_rubrics_keyboard(selected_rubrics=None):
    """Создаёт клавиатуру с рубриками (по 2 в ряд)"""
    if selected_rubrics is None:
        selected_rubrics = []
    
    keyboard = []
    row = []
    
    for i, rubric in enumerate(RUBRICS):
        # Если рубрика уже выбрана, добавляем галочку
        display_name = rubric["name"]
        if rubric["callback"] in selected_rubrics:
            display_name = f"✅ {display_name}"
        
        button = InlineKeyboardButton(
            display_name, 
            callback_data=f"rubric_{rubric['callback']}"
        )
        
        row.append(button)
        
        # Каждые 2 кнопки - новый ряд
        if len(row) == 2 or i == len(RUBRICS) - 1:
            keyboard.append(row)
            row = []
    
    # Добавляем кнопки управления
    keyboard.append([
        InlineKeyboardButton("✅ Завершить выбор", callback_data="finish_selection"),
        InlineKeyboardButton("❌ Отмена", callback_data="cancel_selection")
    ])
    
    return InlineKeyboardMarkup(keyboard)

def get_unsubscribe_keyboard():
    """Клавиатура для подтверждения отписки"""
    keyboard = [
        [InlineKeyboardButton("✅ Да, отписаться", callback_data="confirm_unsubscribe")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard():
    """Клавиатура после завершения выбора"""
    keyboard = [
        [InlineKeyboardButton("📰 Получить новости сейчас", callback_data="get_news_now")],
        [InlineKeyboardButton("⏰ Будут приходить в 8:00", callback_data="daily_only")],
        [InlineKeyboardButton("❌ Отписаться от рассылки", callback_data="start_unsubscribe")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu_keyboard():
    """Клавиатура для возврата в главное меню"""
    keyboard = [
        [InlineKeyboardButton("🔙 В главное меню", callback_data="back_to_menu")],
        [InlineKeyboardButton("📰 Обновить новости", callback_data="get_news_now")]
    ]
    return InlineKeyboardMarkup(keyboard)