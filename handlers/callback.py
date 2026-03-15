from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import json

from database import get_user, save_user, unsubscribe_user
from keyboards import (
    get_rubrics_keyboard, 
    get_unsubscribe_keyboard, 
    get_confirmation_keyboard,
    get_back_to_menu_keyboard
)
from config import MAX_RUBRICS, RUBRICS
from rss_parser import get_news_for_rubrics


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех callback-запросов (нажатий на кнопки)"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Инициализируем выбранные рубрики, если их нет
    if 'selected_rubrics' not in context.user_data:
        context.user_data['selected_rubrics'] = []
    
    # --- ВЫБОР РУБРИКИ ---
    if callback_data.startswith('rubric_'):
        rubric_key = callback_data.replace('rubric_', '')
        
        # Находим название рубрики
        rubric_name = next((r["name"] for r in RUBRICS if r["callback"] == rubric_key), rubric_key)
        
        # Проверяем, выбрана ли уже
        if rubric_key in context.user_data['selected_rubrics']:
            # Убираем из выбора
            context.user_data['selected_rubrics'].remove(rubric_key)
            await query.edit_message_text(
                f"Рубрика {rubric_name} убрана из выбора.\n"
                f"Выбрано: {len(context.user_data['selected_rubrics'])}/{MAX_RUBRICS}",
                reply_markup=get_rubrics_keyboard(context.user_data['selected_rubrics'])
            )
        else:
            # Проверяем лимит
            if len(context.user_data['selected_rubrics']) >= MAX_RUBRICS:
                await query.edit_message_text(
                    f"❌ Вы уже выбрали максимальное количество рубрик ({MAX_RUBRICS}).\n"
                    "Чтобы изменить выбор, уберите какие-нибудь рубрики.",
                    reply_markup=get_rubrics_keyboard(context.user_data['selected_rubrics'])
                )
                return
            
            # Добавляем рубрику
            context.user_data['selected_rubrics'].append(rubric_key)
            await query.edit_message_text(
                f"✅ Рубрика {rubric_name} добавлена!\n"
                f"Выбрано: {len(context.user_data['selected_rubrics'])}/{MAX_RUBRICS}",
                reply_markup=get_rubrics_keyboard(context.user_data['selected_rubrics'])
            )
    
    # --- ЗАВЕРШЕНИЕ ВЫБОРА ---
    elif callback_data == 'finish_selection':
        selected = context.user_data.get('selected_rubrics', [])
        
        if not selected:
            await query.edit_message_text(
                "❌ Вы не выбрали ни одной рубрики. Пожалуйста, выберите хотя бы одну.",
                reply_markup=get_rubrics_keyboard()
            )
            return
        
        # Сохраняем в базу данных
        save_user(
            user_id=user.id,
            chat_id=chat_id,
            username=user.username or "",
            rubrics=selected
        )
        
        # Формируем список выбранных рубрик для красивого вывода
        rubric_names = []
        for r in selected:
            name = next((rub["name"] for rub in RUBRICS if rub["callback"] == r), r)
            rubric_names.append(name)
        
        await query.edit_message_text(
            f"✅ Вы подписались на рубрики:\n\n"
            f"{chr(10).join(['• ' + name for name in rubric_names])}\n\n"
            f"Вы будете получать дайджест ежедневно в 8:00 МСК.",
            reply_markup=get_confirmation_keyboard()
        )
    
    # --- ПОЛУЧИТЬ НОВОСТИ СЕЙЧАС ---
    elif callback_data == 'get_news_now':
        # Получаем рубрики пользователя из базы
        user_data = get_user(user.id)
        if not user_data:
            await query.edit_message_text(
                "❌ Сначала выберите рубрики через /start"
            )
            return
        
        # Парсим рубрики из базы
        rubrics = json.loads(user_data[3]) if user_data[3] else []  # rubrics в 4-й колонке
        
        if not rubrics:
            await query.edit_message_text(
                "❌ У вас нет выбранных рубрик. Нажмите /start чтобы выбрать."
            )
            return
        
        # Отправляем сообщение о начале загрузки
        await query.edit_message_text(
            "📰 Загружаю свежие новости... Это займёт несколько секунд."
        )
        
        # Собираем свежие новости (fresh=True)
        news_data = get_news_for_rubrics(rubrics, fresh=True)
        
        if not news_data:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Не удалось загрузить новости. Попробуйте позже."
            )
            return
        
        # Формируем дайджест
        digest = f"📰 *Свежие новости на {datetime.now().strftime('%d.%m.%Y %H:%M')}*\n\n"
        
        for rubric_data in news_data:
            digest += f"*{rubric_data['rubric']}*\n"
            for i, item in enumerate(rubric_data['news'], 1):
                digest += f"{i}. [{item['title']}]({item['link']})\n"
            digest += "\n"
        
        digest += "\n✨ Чтобы обновить, нажмите кнопку ниже"
        
        # Отправляем дайджест
        await context.bot.send_message(
            chat_id=chat_id,
            text=digest,
            parse_mode='Markdown',
            disable_web_page_preview=False,
            reply_markup=get_back_to_menu_keyboard()
        )
    
    # --- ТОЛЬКО ЕЖЕДНЕВНАЯ РАССЫЛКА ---
    elif callback_data == 'daily_only':
        await query.edit_message_text(
            "✅ Отлично! Теперь вы будете получать дайджест ежедневно в 8:00 МСК.\n\n"
            "Чтобы получить новости прямо сейчас, нажмите /start и выберите 'Получить новости сейчас'."
        )
    
    # --- ВОЗВРАТ В ГЛАВНОЕ МЕНЮ ---
    elif callback_data == 'back_to_menu':
        # Получаем рубрики пользователя из базы
        user_data = get_user(user.id)
        if user_data and user_data[3]:  # если есть рубрики
            await query.edit_message_text(
                "🏠 Главное меню",
                reply_markup=get_confirmation_keyboard()
            )
        else:
            await query.edit_message_text(
                "🏠 Главное меню\n\nЧтобы выбрать рубрики, отправьте /start"
            )
    
    # --- НАЧАЛО ПРОЦЕССА ОТПИСКИ ---
    elif callback_data == 'start_unsubscribe':
        await query.edit_message_text(
            "Вы уверены, что хотите отписаться от рассылки?",
            reply_markup=get_unsubscribe_keyboard()
        )
    
    # --- ПОДТВЕРЖДЕНИЕ ОТПИСКИ ---
    elif callback_data == 'confirm_unsubscribe':
        unsubscribe_user(user.id)
        context.user_data['selected_rubrics'] = []
        await query.edit_message_text(
            "✅ Вы отписались от рассылки.\n"
            "Чтобы подписаться снова, отправьте /start"
        )
    
    # --- ОТМЕНА ВЫБОРА ---
    elif callback_data == 'cancel_selection':
        context.user_data['selected_rubrics'] = []
        await query.edit_message_text(
            "❌ Выбор отменён. Чтобы начать заново, отправьте /start"
        )
    
    # --- НЕИЗВЕСТНЫЙ CALLBACK ---
    else:
        await query.edit_message_text("❌ Неизвестная команда")