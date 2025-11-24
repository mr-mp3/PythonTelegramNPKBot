from telebot import types
from config import Config


def get_genres_keyboard():
    config = Config()
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(genre, callback_data=f"genre_{genre}")
        for genre in config.GENRES
    ]

    for i in range(0, len(buttons), 2):
        row_buttons = [buttons[i]]
        if i + 1 < len(buttons):
            row_buttons.append(buttons[i + 1])
        markup.add(*row_buttons)

    return markup


def get_movies_keyboard(movies, genre, page, total_pages):
    """Создает клавиатуру с фильмами и пагинацией"""
    markup = types.InlineKeyboardMarkup(row_width=1)

    # Кнопки фильмов
    for i, movie in enumerate(movies, (page - 1) * 10 + 1):
        title = movie.get('name', 'Без названия')
        year = movie.get('year', '')

        # Форматируем рейтинг
        rating = movie.get('rating', {}).get('kp')
        if rating and rating != 0 and rating != '0':
            rating_text = f" ⭐{rating}"
        else:
            rating_text = ""

        button_text = f"{i}. {title} ({year}){rating_text}"

        if len(button_text) > 50:
            button_text = button_text[:47] + "..."

        markup.add(types.InlineKeyboardButton(
            button_text,
            callback_data=f"movie_{movie['id']}"
        ))

    # Кнопки пагинации
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(types.InlineKeyboardButton(
            "⬅️ Назад",
            callback_data=f"page_{genre}_{page - 1}"
        ))

    if page < total_pages:
        pagination_buttons.append(types.InlineKeyboardButton(
            "Вперед ➡️",
            callback_data=f"page_{genre}_{page + 1}"
        ))

    if pagination_buttons:
        markup.row(*pagination_buttons)

    # Кнопка возврата к жанрам
    markup.add(types.InlineKeyboardButton(
        "⬅️ Назад к жанрам",
        callback_data="back_to_genres"
    ))

    return markup