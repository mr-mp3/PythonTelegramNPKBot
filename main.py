import sqlite3
import telebot
import requests
import logging
from urllib.parse import quote

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = '8443877498:AAFDoZSnzzQksrEHESwlj6qqQ2aFiK60JSs'
KINOPOISK_API_KEY = 'C0VEPJ3-0J24GPR-GEJX8RP-6TA66FK'  # Получите на https://kinopoisk.dev/
KINOPOISK_API_URL = 'https://api.kinopoisk.dev/v1.4'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Заголовки для API запросов
API_HEADERS = {
    'X-API-KEY': KINOPOISK_API_KEY,
    'Content-Type': 'application/json'
}


def make_kinopoisk_request(endpoint, params=None):
    """Универсальная функция для запросов к API Кинопоиска"""
    try:
        url = f"{KINOPOISK_API_URL}/{endpoint}"
        logger.info(f"Отправка запроса к: {url}")
        logger.info(f"Параметры: {params}")

        response = requests.get(url, headers=API_HEADERS, params=params, timeout=15)

        logger.info(f"Статус код: {response.status_code}")

        if response.status_code == 401:
            return None, "❌ Неверный API ключ. Проверьте ваш X-API-KEY"
        elif response.status_code == 402:
            return None, "❌ Закончился лимит запросов. Попробуйте завтра."
        elif response.status_code == 404:
            return None, "❌ Фильм не найден"
        elif response.status_code == 429:
            return None, "❌ Слишком много запросов. Подождите немного."
        elif response.status_code != 200:
            return None, f"❌ Ошибка API: {response.status_code}"

        data = response.json()
        return data, None

    except requests.exceptions.Timeout:
        logger.error("Таймаут при запросе к API")
        return None, "❌ Таймаут при запросе к API"
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка соединения с API")
        return None, "❌ Ошибка соединения с API. Проверьте интернет-соединение."
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return None, f"❌ Неизвестная ошибка: {e}"


# Функция для сохранения запросов в БД
def save_to_db(user_id, username, request_text):
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user_requests (user_id, username, request_text) VALUES (?, ?, ?)',
            (user_id, username, request_text)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при сохранении в БД: {e}")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🎬 Привет! Я кино-бот с интеграцией Кинопоиска!

Доступные команды:
/search <название> - поиск фильмов
/movie <id> - информация о фильме по ID
/random - случайный фильм
/top - топ фильмов
/popular - популярные фильмы
/help - помощь

Примеры: 
/search матрица
/movie 326
/random
"""
    bot.reply_to(message, welcome_text)


# Поиск фильмов
@bot.message_handler(commands=['search'])
def search_movies(message):
    try:
        command_parts = message.text.split(' ', 1)
        if len(command_parts) < 2:
            bot.reply_to(message, "❌ Укажите название фильма. Например: /search матрица")
            return

        query = command_parts[1].strip()
        if not query:
            bot.reply_to(message, "❌ Пустой запрос")
            return

        bot.send_chat_action(message.chat.id, 'typing')

        # Параметры запроса
        params = {
            'query': query,
            'limit': 5,  # Ограничиваем количество результатов
            'selectFields': ['id', 'name', 'year', 'description', 'rating', 'poster', 'genres', 'countries']
        }

        # Отправляем запрос к API
        data, error = make_kinopoisk_request('movie/search', params=params)

        if error:
            bot.reply_to(message, error)
            return

        if data and data.get('docs') and len(data['docs']) > 0:
            # Отправляем первый результат
            movie = data['docs'][0]
            send_movie_info(message, movie, f"Поиск: {query}")

            # Если есть еще результаты, показываем список
            if len(data['docs']) > 1:
                other_results = "\n\n🎯 Другие найденные фильмы:\n"
                for i, other_movie in enumerate(data['docs'][1:4], 1):
                    title = other_movie.get('name', 'Без названия')
                    year = other_movie.get('year', '')
                    other_results += f"{i}. {title} ({year}) - /movie_{other_movie['id']}\n"

                bot.reply_to(message, other_results)

        else:
            bot.reply_to(message, f"❌ По запросу '{query}' ничего не найдено.")

    except Exception as e:
        logger.error(f"Ошибка в search_movies: {e}")
        bot.reply_to(message, "❌ Произошла внутренняя ошибка при поиске.")


# Обработчик для быстрого доступа к фильму по ID через команду
@bot.message_handler(regexp=r'^/movie_(\d+)$')
def quick_movie_info(message):
    try:
        movie_id = message.text.split('_')[1]
        bot.send_chat_action(message.chat.id, 'typing')

        data, error = make_kinopoisk_request(f'movie/{movie_id}')

        if error:
            bot.reply_to(message, error)
            return

        if data:
            send_movie_info(message, data, f"Быстрый доступ ID: {movie_id}")
        else:
            bot.reply_to(message, f"❌ Фильм с ID {movie_id} не найден.")

    except Exception as e:
        logger.error(f"Ошибка в quick_movie_info: {e}")
        bot.reply_to(message, "❌ Произошла внутренняя ошибка.")


# Получение информации о фильме по ID
@bot.message_handler(commands=['movie'])
def get_movie_by_id(message):
    try:
        command_parts = message.text.split(' ', 1)
        if len(command_parts) < 2:
            bot.reply_to(message, "❌ Укажите ID фильма. Например: /movie 326")
            return

        movie_id = command_parts[1].strip()
        bot.send_chat_action(message.chat.id, 'typing')

        data, error = make_kinopoisk_request(f'movie/{movie_id}')

        if error:
            bot.reply_to(message, error)
            return

        if data:
            send_movie_info(message, data, f"Фильм по ID: {movie_id}")
        else:
            bot.reply_to(message, f"❌ Фильм с ID {movie_id} не найден.")

    except Exception as e:
        logger.error(f"Ошибка в get_movie_by_id: {e}")
        bot.reply_to(message, "❌ Произошла внутренняя ошибка.")


def send_movie_info(message, movie, search_query):
    """Отправляет информацию о фильме"""
    try:
        # Извлекаем информацию о фильме
        title = movie.get('name', 'Название не указано')
        year = movie.get('year', 'Год не указан')
        description = movie.get('description', 'Описание отсутствует')

        # Рейтинг
        rating = movie.get('rating', {})
        kp_rating = rating.get('kp', 'Н/Д')
        imdb_rating = rating.get('imdb', 'Н/Д')

        # Жанры
        genres = []
        if movie.get('genres'):
            genres = [genre.get('name', '') for genre in movie['genres']]
        genres_text = ', '.join(genres) if genres else 'Не указаны'

        # Страны
        countries = []
        if movie.get('countries'):
            countries = [country.get('name', '') for country in movie['countries']]
        countries_text = ', '.join(countries) if countries else 'Не указаны'

        # Длительность
        movie_length = movie.get('movieLength', 'Не указана')

        # Возрастной рейтинг
        age_rating = movie.get('ageRating', 'Не указан')

        # Обрезаем длинное описание
        if description and len(description) > 500:
            description = description[:500] + '...'

        # Формируем текст ответа
        response_text = f"""
🎬 <b>{title}</b> ({year})

⭐ Рейтинг КП: <b>{kp_rating}</b>
⭐ Рейтинг IMDb: <b>{imdb_rating}</b>

🎭 Жанры: {genres_text}
🌍 Страны: {countries_text}
⏱ Длительность: {movie_length} мин
🔞 Возрастной рейтинг: {age_rating}+
🆔 ID: {movie.get('id', 'Не указан')}

📖 {description}
        """.strip()

        # Пробуем отправить с постером
        poster_url = None
        if movie.get('poster') and movie.get('poster').get('url'):
            poster_url = movie['poster']['url']

        if poster_url:
            try:
                bot.send_photo(
                    message.chat.id,
                    poster_url,
                    caption=response_text,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Ошибка отправки фото: {e}")
                bot.reply_to(message, response_text, parse_mode='HTML')
        else:
            bot.reply_to(message, response_text, parse_mode='HTML')

        # Сохраняем запрос в БД
        save_to_db(message.from_user.id, message.from_user.username, search_query)

    except Exception as e:
        logger.error(f"Ошибка в send_movie_info: {e}")
        bot.reply_to(message, "❌ Ошибка при формировании ответа.")


# Случайный фильм
@bot.message_handler(commands=['random'])
def random_movie(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        data, error = make_kinopoisk_request('movie/random')

        if error:
            bot.reply_to(message, error)
            return

        if data:
            send_movie_info(message, data, "Случайный фильм")
        else:
            bot.reply_to(message, "❌ Не удалось получить случайный фильм")

    except Exception as e:
        logger.error(f"Ошибка в random_movie: {e}")
        bot.reply_to(message, "❌ Произошла ошибка при получении случайного фильма")


# Топ фильмов
@bot.message_handler(commands=['top'])
def top_movies(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        params = {
            'lists': 'top250',
            'limit': 10,
            'selectFields': ['id', 'name', 'year', 'rating']
        }

        data, error = make_kinopoisk_request('movie', params=params)

        if error:
            bot.reply_to(message, error)
            return

        if data and data.get('docs') and len(data['docs']) > 0:
            response_text = "🏆 <b>Топ-10 фильмов Кинопоиска:</b>\n\n"

            for i, movie in enumerate(data['docs'], 1):
                title = movie.get('name', 'Без названия')
                year = movie.get('year', '')
                rating = movie.get('rating', {}).get('kp', 'Н/Д')
                movie_id = movie.get('id', '')

                response_text += f"{i}. <b>{title}</b> ({year}) - ⭐ {rating} - /movie_{movie_id}\n"

            bot.reply_to(message, response_text, parse_mode='HTML')
            save_to_db(message.from_user.id, message.from_user.username, "Запрос топа фильмов")
        else:
            bot.reply_to(message, "❌ Не удалось загрузить топ фильмов")

    except Exception as e:
        logger.error(f"Ошибка в top_movies: {e}")
        bot.reply_to(message, "❌ Произошла ошибка при получении топа фильмов")


# Популярные фильмы
@bot.message_handler(commands=['popular'])
def popular_movies(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        params = {
            'sortField': 'votes.kp',
            'sortType': '-1',
            'limit': 10,
            'selectFields': ['id', 'name', 'year', 'rating', 'votes']
        }

        data, error = make_kinopoisk_request('movie', params=params)

        if error:
            bot.reply_to(message, error)
            return

        if data and data.get('docs') and len(data['docs']) > 0:
            response_text = "🔥 <b>Популярные фильмы:</b>\n\n"

            for i, movie in enumerate(data['docs'], 1):
                title = movie.get('name', 'Без названия')
                year = movie.get('year', '')
                rating = movie.get('rating', {}).get('kp', 'Н/Д')
                votes = movie.get('votes', {}).get('kp', 0)
                movie_id = movie.get('id', '')

                response_text += f"{i}. <b>{title}</b> ({year}) - ⭐ {rating} (голосов: {votes}) - /movie_{movie_id}\n"

            bot.reply_to(message, response_text, parse_mode='HTML')
            save_to_db(message.from_user.id, message.from_user.username, "Запрос популярных фильмов")
        else:
            bot.reply_to(message, "❌ Не удалось загрузить популярные фильмы")

    except Exception as e:
        logger.error(f"Ошибка в popular_movies: {e}")
        bot.reply_to(message, "❌ Произошла ошибка при получении популярных фильмов")


# Команда помощи
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🤖 Помощь по боту:

Основные команды:
/start - начать работу
/search <название> - поиск фильмов
/movie <id> - информация о фильме по ID
/random - случайный фильм
/top - топ-10 фильмов Кинопоиска
/popular - популярные фильмы
/help - эта справка

Примеры:
/search матрица
/movie 326
/random

💡 Подсказки:
• Используйте команды из результатов поиска для быстрого доступа
• ID фильма можно найти в результатах поиска
"""
    bot.reply_to(message, help_text)


# Проверка API
@bot.message_handler(commands=['test'])
def test_api(message):
    """Команда для проверки работы API"""
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        data, error = make_kinopoisk_request('movie/326')  # Проверяем на примере фильма "Побег из Шоушенка"

        if error:
            bot.reply_to(message, f"❌ Ошибка API: {error}")
        else:
            bot.reply_to(message, f"✅ API работает корректно! Лимиты: {data.get('limit', 'N/A')}")

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при тесте: {e}")


if __name__ == '__main__':
    logger.info("Бот запускается...")

    # Проверяем наличие API ключа
    if KINOPOISK_API_KEY == 'YOUR_KINOPOISK_API_KEY':
        logger.error("❌ ВНИМАНИЕ: Установите ваш KINOPOISK_API_KEY в коде!")
        print("❌ ВНИМАНИЕ: Установите ваш KINOPOISK_API_KEY в коде!")

    logger.info("Бот запущен")
    print("Бот запущен...")

    try:
        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"Ошибка при запуске бота: {e}")