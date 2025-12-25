from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services.kinopoisk_api import search_movie
from services.database import get_filters
from utils.formatters import format_movie
from utils.states import SearchStates
from keyboards.back import back_keyboard

router = Router()


@router.message(Command("search"))
async def start_search(message: Message, state: FSMContext):
    await message.answer("🔍 Введите название фильма:")
    await state.set_state(SearchStates.waiting_for_query)


@router.message(SearchStates.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    query = message.text.strip()

    filters = get_filters(message.from_user.id)
    year, rating = filters if filters else (None, None)

    movies, error = search_movie(query, year, rating)

    if error:
        await message.answer(error)
        await state.clear()
        return

    movie = movies[0]
    text, poster = format_movie(movie)

    if poster:
        await message.answer_photo(photo=poster, caption=text)
    else:
        await message.answer(text)

    await state.clear()
