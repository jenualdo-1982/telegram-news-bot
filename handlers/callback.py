from telegram import Update
from telegram.ext import ContextTypes
from database import save_user, update_user_rubrics, unsubscribe_user
from keyboards import get_rubrics_keyboard, get_unsubscribe_keyboard, get_confirmation_keyboard
from config import MAX_RUBRICS, RUBRICS

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
    
    # Выбор рубрики
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
    
    # Завершение выбора
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
    
    # Отмена выбора
    elif callback_data == 'cancel_selection':
        context.user_data['selected_rubrics'] = []
        await query.edit_message_text(
            "❌ Выбор отменён. Чтобы начать заново, отправьте /start"
        )
    
    # Начало процесса отписки
    elif callback_data == 'start_unsubscribe':
        await query.edit_message_text(
            "Вы уверены, что хотите отписаться от рассылки?",
            reply_markup=get_unsubscribe_keyboard()
        )
    
    # Подтверждение отписки
    elif callback_data == 'confirm_unsubscribe':
        unsubscribe_user(user.id)
        context.user_data['selected_rubrics'] = []
        await query.edit_message_text(
            "✅ Вы отписались от рассылки.\n"
            "Чтобы подписаться снова, отправьте /start"
        )
    
    # Получить новости сейчас
    elif callback_data == 'get_news_now':
        await query.edit_message_text(
            "📰 Функция получения новостей сейчас будет добавлена в следующей версии.\n"
            "Пока что новости приходят автоматически в 8:00."
        )
    
    # Неизвестный callback
    else:
        await query.edit_message_text("❌ Неизвестная команда")