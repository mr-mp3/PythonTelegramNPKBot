from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.kinopoisk_api import get_random_movie, get_top_movies
from utils.formatters import format_movie

router = Router()


@router.message(Command("random"))
async def random_movie_handler(message: Message):
    """
    Отправляет случайный фильм
    """
    await message.answer("🎲 Ищу случайный фильм...")

    movie, error = get_random_movie()

    if error:
        await message.answer(error)
        return

    text, poster = format_movie(movie)

    if poster:
        await message.answer_photo(photo=poster, caption=text)
    else:
        await message.answer(text)


@router.message(Command("top"))
async def top_movies_handler(message: Message):
    """
    Отправляет топ-10 фильмов
    """
    await message.answer("🏆 Загружаю топ фильмов...")

    movies, error = get_top_movies(limit=10)

    if error:
        await message.answer(error)
        return

    response = "🏆 <b>Топ-10 фильмов Кинопоиска</b>\n\n"

    for index, movie in enumerate(movies, start=1):
        title = movie.get("name", "Без названия")
        year = movie.get("year", "")
        rating = movie.get("rating", {}).get("kp")

        line = f"{index}. <b>{title}</b>"
        if year:
            line += f" ({year})"
        if rating:
            line += f" — ⭐ {rating}"

        response += line + "\n"

    await message.answer(response)
