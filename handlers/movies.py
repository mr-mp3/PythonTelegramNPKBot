from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from services.kinopoisk_api import get_random_movie, get_top_movies
from utils.formatters import format_movie, format_rating
from keyboards.back import back_keyboard
from keyboards.random_retry import random_retry_keyboard

router = Router()


# ====== ТОП ФИЛЬМОВ ======

@router.message(Command("top"))
async def top_movies_handler(message: Message):
    await message.answer("🏆 Загружаю топ фильмов...")

    movies, error = get_top_movies(limit=10)

    if error:
        await message.answer(error, reply_markup=back_keyboard())
        return

    response = "🏆 <b>Топ-10 фильмов Кинопоиска</b>\n\n"

    for index, movie in enumerate(movies, start=1):
        title = movie.get("name", "Без названия")
        year = movie.get("year", "—")

        # 🔥 ВАЖНО: ТОЛЬКО ТАК
        rating = format_rating(movie.get("rating", {}).get("kp"))

        response += (
            f"{index}. <b>{title}</b> ({year}) — ⭐ {rating}\n"
        )

    # 🔥 ВАЖНО: reply_markup
    await message.answer(
        response,
        reply_markup=back_keyboard()
    )


# ====== СЛУЧАЙНЫЙ ФИЛЬМ ======

@router.message(Command("random"))
async def random_movie_handler(message: Message):
    await message.answer("🎲 Ищу случайный фильм...")

    movie, error = get_random_movie()

    if error:
        await message.answer(
            error,
            reply_markup=random_retry_keyboard()
        )
        return

    text, poster = format_movie(movie)

    if poster:
        await message.answer_photo(
            poster,
            caption=text,
            reply_markup=back_keyboard()
        )
    else:
        await message.answer(
            text,
            reply_markup=back_keyboard()
        )


# ====== ПОВТОР СЛУЧАЙНОГО ФИЛЬМА ======

@router.callback_query(F.data == "random_retry")
async def random_retry(call: CallbackQuery):
    await call.message.edit_text("🎲 Ищу другой фильм...")

    movie, error = get_random_movie()

    if error:
        await call.message.edit_text(
            error,
            reply_markup=random_retry_keyboard()
        )
        await call.answer()
        return

    text, poster = format_movie(movie)

    if poster:
        await call.message.answer_photo(
            poster,
            caption=text,
            reply_markup=back_keyboard()
        )
    else:
        await call.message.answer(
            text,
            reply_markup=back_keyboard()
        )

    await call.answer()
