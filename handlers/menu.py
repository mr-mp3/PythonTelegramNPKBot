from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.kinopoisk_api import get_random_movie, get_top_movies
from utils.formatters import format_movie, format_rating
from utils.states import SearchStates
from keyboards.back import back_keyboard
from keyboards.filters import filters_keyboard
from keyboards.random_retry import random_retry_keyboard
from keyboards.main_menu import main_menu_keyboard

router = Router()



@router.callback_query(F.data == "menu_search")
async def menu_search(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "🔍 Введите название фильма:",
        reply_markup=back_keyboard()
    )
    await state.set_state(SearchStates.waiting_for_query)
    await call.answer()



@router.callback_query(F.data == "menu_random")
async def menu_random(call: CallbackQuery):
    await call.message.edit_text("🎲 Ищу случайный фильм...")

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



@router.callback_query(F.data == "menu_top")
async def menu_top(call: CallbackQuery):
    await call.message.edit_text("🏆 Загружаю топ фильмов...")

    movies, error = get_top_movies(limit=10)

    if error:
        await call.message.edit_text(
            error,
            reply_markup=back_keyboard()
        )
        await call.answer()
        return

    text = "🏆 <b>Топ-10 фильмов Кинопоиска</b>\n\n"

    for i, movie in enumerate(movies, start=1):
        title = movie.get("name", "Без названия")
        year = movie.get("year", "—")
        rating = format_rating(movie.get("rating", {}).get("kp"))

        text += f"{i}. <b>{title}</b> ({year}) — ⭐ {rating}\n"

    await call.message.edit_text(
        text,
        reply_markup=back_keyboard()
    )
    await call.answer()



@router.callback_query(F.data == "menu_filters")
async def menu_filters(call: CallbackQuery):
    await call.message.edit_text(
        "🎯 <b>Настройка фильтров</b>\n\nВыберите действие:",
        reply_markup=filters_keyboard()
    )
    await call.answer()



@router.callback_query(F.data == "menu_back")
async def menu_back(call: CallbackQuery):
    await call.message.answer("🎬 Выберите действие:", reply_markup=main_menu_keyboard())
    try:
        await call.message.delete()
    except:
        pass
