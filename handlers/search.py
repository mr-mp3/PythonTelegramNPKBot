from .base import BaseHandler
from utils.formatters import format_movie_info, format_rating
import logging

logger = logging.getLogger(__name__)


class SearchHandlers(BaseHandler):
    def setup_handlers(self):
        # УБИРАЕМ отсюда команду /start, она теперь в commands.py
        @self.bot.message_handler(commands=['search'])
        def search_movies(message):
            self._handle_search(message)

        @self.bot.message_handler(commands=['random'])
        def random_movie(message):
            self._handle_random_movie(message)

        @self.bot.message_handler(commands=['top'])
        def top_movies(message):
            self._handle_top_movies(message)

    def _handle_search(self, message):
        try:
            command_parts = message.text.split(' ', 1)
            if len(command_parts) < 2:
                self.bot.reply_to(message, "❌ Укажите название фильма. Например: /search матрица")
                return

            query = command_parts[1].strip()
            self.bot.send_chat_action(message.chat.id, 'typing')

            data, error = self.kinopoisk.search_movies(query, limit=1)

            if error or not data or not data.get('docs'):
                self.bot.reply_to(message, f"❌ По запросу '{query}' ничего не найдено.")
                return

            movie = data['docs'][0]
            self._send_movie_info(message.chat.id, movie)
            self.database.save_request(
                message.from_user.id,
                message.from_user.username,
                f"Поиск: {query}"
            )

        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            self.bot.reply_to(message, "❌ Ошибка при поиске.")

    def _handle_random_movie(self, message):
        try:
            self.bot.send_chat_action(message.chat.id, 'typing')
            data, error = self.kinopoisk.get_random_movie()

            if error or not data:
                self.bot.reply_to(message, "❌ Не удалось получить случайный фильм")
                return

            self._send_movie_info(message.chat.id, data)
            self.database.save_request(
                message.from_user.id,
                message.from_user.username,
                "Случайный фильм"
            )

        except Exception as e:
            logger.error(f"Ошибка случайного фильма: {e}")
            self.bot.reply_to(message, "❌ Ошибка при получении фильма")

    def _handle_top_movies(self, message):
        try:
            self.bot.send_chat_action(message.chat.id, 'typing')

            data, error = self.kinopoisk.get_top_movies(limit=10)

            if error or not data or not data.get('docs'):
                self.bot.reply_to(message, "❌ Не удалось загрузить топ фильмов")
                return

            response_text = "🏆 <b>Топ-10 фильмов Кинопоиска:</b>\n\n"

            for i, movie in enumerate(data['docs'], 1):
                title = movie.get('name', 'Без названия')
                year = movie.get('year', '')
                rating = format_rating(movie.get('rating', {}).get('kp'))

                movie_text = f"{i}. <b>{title}</b> ({year})"
                if rating:
                    movie_text += f" - ⭐ {rating}"

                response_text += movie_text + "\n"

            self.bot.reply_to(message, response_text, parse_mode='HTML')
            self.database.save_request(
                message.from_user.id,
                message.from_user.username,
                "Запрос топа фильмов"
            )

        except Exception as e:
            logger.error(f"Ошибка топа: {e}")
            self.bot.reply_to(message, "❌ Ошибка при получении топа")

    def _send_movie_info(self, chat_id, movie):
        try:
            response_text, poster_url = format_movie_info(movie)

            if poster_url:
                try:
                    self.bot.send_photo(
                        chat_id,
                        poster_url,
                        caption=response_text,
                        parse_mode='HTML'
                    )
                    return
                except Exception as e:
                    logger.error(f"Ошибка отправки фото: {e}")

            self.bot.send_message(chat_id, response_text, parse_mode='HTML')

        except Exception as e:
            logger.error(f"Ошибка отправки информации: {e}")
            self.bot.send_message(chat_id, "❌ Ошибка при формировании ответа.")