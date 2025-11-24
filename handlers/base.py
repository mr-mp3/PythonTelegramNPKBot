from database import Database
from kinopoisk import KinopoiskAPI

class BaseHandler:
    def __init__(self, bot, user_data=None):
        self.bot = bot
        self.user_data = user_data or {}
        self.database = Database()
        self.kinopoisk = KinopoiskAPI()