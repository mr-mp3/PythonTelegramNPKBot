import logging
from telebot import types
from .base import BaseHandler
from utils.formatters import format_movie_info
from utils.keyboards import get_genres_keyboard, get_movies_keyboard

logger = logging.getLogger(__name__)


class MovieHandlers(BaseHandler):
    def setup_handlers(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
        def handle_page_change(call):
            self._handle_page_change(call)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('movie_'))
        def handle_movie_selection(call):
            self._handle_movie_selection(call)

    def _show_movies_page(self, message, user_id, genre, page):
        """Показывает страницу с фильмами"""
        limit = 10

        # Получаем фильмы из API
        data, error = self.kinopoisk.get_movies_by_genre(genre, page, limit)

        if error or not data or not data.get('docs'):
            error_msg = f"❌ Не удалось найти фильмы в жанре '{genre}'"
            if hasattr(message, 'message_id'):
                self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    text=error_msg
                )
            else:
                self.bot.send_message(message.chat.id, error_msg)
            return

        movies = data['docs']
        total_movies = data.get('total', 0)
        total_pages = max(1, (total_movies + limit - 1) // limit)

        # Сохраняем информацию о текущем просмотре
        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        self.user_data[user_id].update({
            'selected_genre': genre,
            'current_page': page,
            'total_pages': total_pages
        })

        # Создаем клавиатуру
        markup = get_movies_keyboard(movies, genre, page, total_pages)

        # Отправляем или обновляем сообщение
        text = f"🎬 Фильмы в жанре '{genre}' (стр. {page}/{total_pages}):"

        if hasattr(message, 'message_id'):
            try:
                self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    text=text,
                    reply_markup=markup
                )
            except Exception as e:
                logger.error(f"Ошибка редактирования сообщения: {e}")
                # Если не удалось редактировать, отправляем новое
                self.bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, text, reply_markup=markup)

    def _handle_page_change(self, call):
        """Обрабатывает смену страницы"""
        try:
            # Извлекаем жанр и номер страницы из callback_data
            # Формат: page_жанр_номер_страницы
            parts = call.data.split('_')
            if len(parts) < 3:
                self.bot.answer_callback_query(call.id, "❌ Ошибка в данных пагинации")
                return

            genre = parts[1]
            page = int(parts[2])

            self.bot.answer_callback_query(call.id, f"Загружаем страницу {page}...")
            self._show_movies_page(call.message, call.from_user.id, genre, page)

        except Exception as e:
            logger.error(f"Ошибка при смене страницы: {e}")
            self.bot.answer_callback_query(call.id, "❌ Ошибка при загрузке страницы")

    def _handle_movie_selection(self, call):
        """Обрабатывает выбор фильма"""
        movie_id = call.data.replace('movie_', '')
        user_id = call.from_user.id

        self.bot.answer_callback_query(call.id, "Загружаем информацию о фильме...")

        # Получаем информацию о фильме
        data, error = self.kinopoisk.get_movie(movie_id)

        if error or not data:
            self.bot.send_message(call.message.chat.id, "❌ Не удалось загрузить информацию о фильме")
            return

        # Отправляем информацию о фильме
        self._send_movie_info(call.message.chat.id, data)

        # Сохраняем запрос в БД
        genre = self.user_data.get(user_id, {}).get('selected_genre', 'неизвестно')
        self.database.save_request(
            user_id,
            call.from_user.username,
            f"Фильм по жанру: {genre}"
        )

    def _send_movie_info(self, chat_id, movie):
        """Отправляет информацию о фильме"""
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