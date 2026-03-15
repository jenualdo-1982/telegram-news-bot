import os

# Токен бота (получить у @BotFather)
BOT_TOKEN = "TOKEN"

# Список рубрик с их callback_data и эмодзи
RUBRICS = [
    {"name": "⚽ Спорт-Экспресс", "callback": "s-expr", "rss": "https://www.sport-express.ru/services/materials/news/se/"},
    {"name": "🌍 Мир", "callback": "world", "rss": "https://news.un.org/feed/subscribe/ru/news/all/rss.xml"},
    {"name": "🇪🇺 Европа", "callback": "europe", "rss": "https://ru.euronews.com/rss"},
    {"name": "🇷🇺 Россия", "callback": "russia", "rss": "https://tass.ru/rss/v2.xml"},
    {"name": "💼 Экономика", "callback": "economy", "rss": "https://quote.ru/rss"},
    {"name": "📈 Финансы", "callback": "finance", "rss": "https://fomag.ru/news/rss/"},
    {"name": "🤖 AI", "callback": "ai", "rss": "https://news.mit.edu/topic/mitartificial-intelligence-rss.xml"},
    {"name": "💻 Технологии", "callback": "tech", "rss": "https://techcrunch.com/feed/"},
    {"name": "🚀 Стартапы", "callback": "startup", "rss": "https://vc.ru/rss"},
    {"name": "🔬 Наука", "callback": "science", "rss": "https://nauka.tass.ru/rss"},
    {"name": "🏥 Медицина", "callback": "medicine", "rss": "https://medvestnik.ru/content/novosti/rss"},
    {"name": "🌱 Экология", "callback": "eco", "rss": "https://greenpeace.ru/rss"},
    {"name": "⚡ Энергетика", "callback": "energy", "rss": "https://neftegaz.ru/export/rss/"},
    {"name": "🏛 Политика", "callback": "politics", "rss": "https://ria.ru/export/rss2/politics/"},
    {"name": "🎮 Игры", "callback": "games", "rss": "https://stopgame.ru/rss/news"},
    {"name": "⚽ Спорт", "callback": "sport", "rss": "https://matchtv.ru/rss"},
    {"name": "🌐 Крипто", "callback": "crypto", "rss": "https://coinmarketcap.com/rss"},
]

# Максимальное количество выбираемых рубрик
MAX_RUBRICS = 5

# Время ежедневной рассылки (час, минута)
DAILY_HOUR = 8
DAILY_MINUTE = 0
TIMEZONE = "Europe/Moscow"

# База данных
DATABASE_PATH = "news_bot.db"