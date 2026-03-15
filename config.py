import os

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Список рубрик с их callback_data и эмодзи
RUBRICS = [
    # Спорт 
    {"name": "⚽ Спорт-Экспресс", "callback": "sport-express", "rss": "https://www.sport-express.ru/services/materials/news/se/"},
    {"name": "⚽ Soccer", "callback": "soccer", "rss": "https://www.soccer.ru/rss"},
    {"name": "⚽ Sports.ru", "callback": "sport-sports", "rss": "https://www.sports.ru/rss/all_news.xml"},
    
    # Мировые новости
    {"name": "🌍 Lenta", "callback": "lenta", "rss": "https://lenta.ru/rss"},
    {"name": "🇷🇺 Россия (ТАСС)", "callback": "russia", "rss": "https://tass.ru/rss/v2.xml"},
    {"name": "🇪🇺 Европа", "callback": "europe", "rss": "https://euro-pulse.ru/feed"},
    
    # Экономика и финансы
    {"name": "💼 Московский комсомолец", "callback": "mk", "rss": "https://www.mk.ru/rss/index.xml"},
    {"name": "📈 Финансы", "callback": "finance", "rss": "https://fomag.ru/news/rss/"},
    {"name": "📈 Столица-С", "callback": "stolica", "rss": "https://stolica-s.su/feed"},
    
    # Технологии и AI
    {"name": "💻 Технологии", "callback": "tech", "rss": "https://techcrunch.com/feed/"},
    {"name": "💻 Habr", "callback": "habr", "rss": "https://habr.com/ru/rss/articles/"},
    
    # Стартапы
    {"name": "🚀 Стартапы", "callback": "startup", "rss": "https://vc.ru/rss"},
    {"name": "🚀 Rusbase", "callback": "rusbase", "rss": "https://rb.ru/feeds/all/"},
    
    # Наука и медицина
    {"name": "🔬 Naked Science", "callback": "naked", "rss": "https://naked-science.ru/feed"},
    
    # Политика
    {"name": "🏛 Ведомости", "callback": "vedomosti", "rss": "https://www.vedomosti.ru/rss/news"},
    
    # Игры (новые рабочие ссылки)
    {"name": "🎮 DTF", "callback": "games-dtf", "rss": "https://dtf.ru/rss/"},
]

# Максимальное количество выбираемых рубрик
MAX_RUBRICS = 5

# Время ежедневной рассылки (час, минута)
DAILY_HOUR = 8
DAILY_MINUTE = 0
TIMEZONE = "Europe/Moscow"

# База данных
DATABASE_PATH = "news_bot.db"