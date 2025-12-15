from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.kinopoisk_api import get_top_movies, get_random_movie
from utils.formatters import format_movie
from utils.states import SearchStates


router = Router()


@router.callback_query(F.data == "menu_top")
async def menu_top(call: CallbackQuery):
    await call.message.edit_text("🏆 Загружаю топ фильмов...")

    movies, error = get_top_movies(limit=10)

    if error:
        await call.message.edit_text(error)
        await call.answer()
        return

    text = "🏆 <b>Топ-10 фильмов Кинопоиска</b>\n\n"

    for i, movie in enumerate(movies, start=1):
        title = movie.get("name", "Без названия")
        year = movie.get("year", "")
        rating = movie.get("rating", {}).get("kp")

        line = f"{i}. <b>{title}</b>"
        if year:
            line += f" ({year})"
        if rating:
            line += f" — ⭐ {rating}"

        text += line + "\n"

    await call.message.edit_text(text)
    await call.answer()


@router.callback_query(F.data == "menu_random")
async def menu_random(call: CallbackQuery):
    await call.message.edit_text("🎲 Ищу случайный фильм...")

    movie, error = get_random_movie()

    if error:
        await call.message.edit_text(error)
        await call.answer()
        return

    text, poster = format_movie(movie)

    if poster:
        await call.message.answer_photo(poster, caption=text)
    else:
        await call.message.answer(text)

    await call.answer()

@router.callback_query(F.data == "menu_search")
async def menu_search(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("🔍 Введите название фильма:")
    await state.set_state(SearchStates.waiting_for_query)
    await call.answer()

from keyboards.filters import filters_keyboard

@router.callback_query(F.data == "menu_filters")
async def menu_filters(call: CallbackQuery):
    await call.message.edit_text(
        "🎯 <b>Настройка фильтров</b>\n\n"
        "Выберите действие:",
        reply_markup=filters_keyboard()
    )
    await call.answer()

