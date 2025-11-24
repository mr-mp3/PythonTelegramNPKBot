from telebot import types
from .base import BaseHandler
from utils.keyboards import get_genres_keyboard


class GenreHandlers(BaseHandler):
    def __init__(self, bot, user_data, config):
        super().__init__(bot, user_data)
        self.config = config

    def setup_handlers(self):
        @self.bot.message_handler(commands=['genres'])
        def show_genres(message):
            self._show_genres_menu(message.chat.id)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('genre_'))
        def handle_genre_selection(call):
            self._handle_genre_selection(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'back_to_genres')
        def handle_back_to_genres(call):
            self._show_genres_menu(call.message.chat.id, call.message.message_id)

    def _show_genres_menu(self, chat_id, message_id=None):
        user_id = chat_id

        # Инициализируем данные пользователя
        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        self.user_data[user_id]['step'] = 'genre_selection'

        markup = get_genres_keyboard()

        if message_id:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="🎬 Выберите жанр фильма:",
                reply_markup=markup
            )
        else:
            self.bot.send_message(
                chat_id,
                "🎬 Выберите жанр фильма:",
                reply_markup=markup
            )

    def _handle_genre_selection(self, call):
        user_id = call.from_user.id
        genre = call.data.replace('genre_', '')

        # Сохраняем выбранный жанр
        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        self.user_data[user_id].update({
            'selected_genre': genre,
            'step': 'movie_selection'
        })

        self.bot.answer_callback_query(call.id, f"Ищем фильмы в жанре {genre}...")

        # Загружаем первую страницу фильмов
        from .movies import MovieHandlers
        movie_handlers = MovieHandlers(self.bot, self.user_data)
        movie_handlers._show_movies_page(call.message, user_id, genre, 1)