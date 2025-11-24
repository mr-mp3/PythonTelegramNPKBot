from .base import BaseHandler

class CommandHandlers(BaseHandler):
    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            welcome_text = """
🎬 Привет! Я кино-бот с Кинопоиском!

Доступные команды:
/genres - выбрать фильм по жанру
/search - поиск фильмов
/random - случайный фильм
/top - топ фильмов

Нажмите /genres чтобы выбрать фильм по жанру!
"""
            self.bot.reply_to(message, welcome_text)