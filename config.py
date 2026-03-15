import os

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Список рубрик с их callback_data и эмодзи
RUBRICS = [
    # Спорт 
    {"name": "⚽ Спорт-Экспресс", "callback": "sport-express", "rss": "https://www.sport-express.ru/services/materials/news/se/"},
    {"name": "⚽ Чемпионат", "callback": "sport-champ", "rss": "https://www.championat.com/news/rss/"},
    {"name": "⚽ Sports.ru", "callback": "sport-sports", "rss": "https://www.sports.ru/rss/all_news.xml"},
    
    # Мировые новости
    {"name": "🌍 Мир (BBC)", "callback": "world-bbc", "rss": "http://feeds.bbci.co.uk/russian/news/rss.xml"},
    {"name": "🇷🇺 Россия (ТАСС)", "callback": "russia", "rss": "https://tass.ru/rss/v2.xml"},
    {"name": "🇪🇺 Европа (Европульс)", "callback": "europe", "rss": "https://euro-pulse.ru/feed"},
    
    # Экономика и финансы
    {"name": "💼 Экономика", "callback": "economy", "rss": "https://quote.ru/rss"},
    {"name": "📈 Финансы", "callback": "finance", "rss": "https://fomag.ru/news/rss/"},
    {"name": "📈 РБК", "callback": "rbc", "rss": "https://rssexport.rbc.ru/rbcnews/news.rss"},
    
    # Технологии и AI
    {"name": "🤖 AI (MIT)", "callback": "ai", "rss": "https://news.mit.edu/topic/mitartificial-intelligence-rss.xml"},
    {"name": "💻 Технологии", "callback": "tech", "rss": "https://techcrunch.com/feed/"},
    {"name": "💻 Habr", "callback": "habr", "rss": "https://habr.com/ru/rss/articles/"},
    
    # Стартапы
    {"name": "🚀 Стартапы", "callback": "startup", "rss": "https://vc.ru/rss"},
    {"name": "🚀 Rusbase", "callback": "rusbase", "rss": "https://rb.ru/feeds/all/"},
    
    # Наука и медицина
    {"name": "🔬 Наука (ТАСС)", "callback": "science", "rss": "https://nauka.tass.ru/rss"},
    {"name": "🔬 Naked Science", "callback": "naked", "rss": "https://naked-science.ru/feed"},
    {"name": "🏥 Медицина", "callback": "medicine", "rss": "https://medvestnik.ru/content/novosti/rss"},
    
    # Экология и энергетика
    {"name": "🌱 Экология", "callback": "eco", "rss": "https://greenpeace.ru/rss"},
    {"name": "⚡ Энергетика", "callback": "energy", "rss": "https://neftegaz.ru/export/rss/"},
    
    # Политика
    {"name": "🏛 Политика (РБК)", "callback": "politics", "rss": "https://rssexport.rbc.ru/rbcnews/news.rss"},
    {"name": "🏛 Ведомости", "callback": "vedomosti", "rss": "https://www.vedomosti.ru/rss/news"},
    
    # Игры (новые рабочие ссылки)
    {"name": "🎮 DTF", "callback": "games-dtf", "rss": "https://dtf.ru/rss/"},
    {"name": "🎮 Kanobu", "callback": "games-kanobu", "rss": "https://kanobu.ru/export/rss.xml"},
    {"name": "🎮 Igromania", "callback": "games-igro", "rss": "https://www.igromania.ru/rss/news/"},
    
    # Крипто
    {"name": "🌐 Крипто (Bits)", "callback": "crypto", "rss": "https://bits.media/rss/"},
    {"name": "🌐 Крипто (ForkLog)", "callback": "forklog", "rss": "https://forklog.com/feed"},
]
]

# Максимальное количество выбираемых рубрик
MAX_RUBRICS = 5

# Время ежедневной рассылки (час, минута)
DAILY_HOUR = 8
DAILY_MINUTE = 0
TIMEZONE = "Europe/Moscow"

# База данных
DATABASE_PATH = "news_bot.db"