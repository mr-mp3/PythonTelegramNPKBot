from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🎬 <b>Привет!</b>\n\n"
        "Я кино-бот с API Кинопоиска.\n"
        "Выбери действие 👇",
        reply_markup=main_menu_keyboard()
    )
