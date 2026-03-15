Telegram-бот для персонализированной рассылки новостей. Пользователи могут выбрать до 5 категорий из 16 доступных и получать ежедневные дайджесты в 8:00 МСК. Также поддерживается получение новостей по запросу.


Установка

 Clone the repository

   ```bash
   git clone https://github.com/yourusername/telegram-news-bot.git
   cd telegram-news-bot

Create virtual environment

bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

Install dependencies

bash
pip install -r requirements.txt

Configure the bot

bash
cp config.py.example config.py
Edit config.py and add your Telegram Bot Token

Run the bot

bash
python bot.py