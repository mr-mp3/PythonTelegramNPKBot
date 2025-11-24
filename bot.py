import logging
from telebot import TeleBot
from config import Config
from handlers.commands import CommandHandlers
from handlers.genres import GenreHandlers
from handlers.movies import MovieHandlers
from handlers.search import SearchHandlers

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.config = Config()
        self.bot = TeleBot(self.config.TELEGRAM_BOT_TOKEN)
        self.user_data = {}

        # Инициализация обработчиков
        self.command_handlers = CommandHandlers(self.bot, self.user_data)
        self.genre_handlers = GenreHandlers(self.bot, self.user_data, self.config)
        self.movie_handlers = MovieHandlers(self.bot, self.user_data)
        self.search_handlers = SearchHandlers(self.bot)

    def setup_handlers(self):
        """Настройка всех обработчиков"""
        self.command_handlers.setup_handlers()
        self.genre_handlers.setup_handlers()
        self.movie_handlers.setup_handlers()
        self.search_handlers.setup_handlers()

    def run(self):
        """Запуск бота"""
        if self.config.KINOPOISK_API_KEY == 'YOUR_KINOPOISK_API_KEY':
            logger.error("❌ ВНИМАНИЕ: Установите ваш KINOPOISK_API_KEY в config.py!")
            return

        self.setup_handlers()
        logger.info("Бот запускается...")
        self.bot.polling(none_stop=True)