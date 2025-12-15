from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.main_menu import main_menu_keyboard

router = Router()

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📌 <b>Команды бота</b>\n\n"
        "🔍 Поиск фильма\n"
        "🎯 Фильтрация\n"
        "🎲 Случайный фильм\n"
        "🏆 Топ фильмов",
        reply_markup=main_menu_keyboard()
    )
