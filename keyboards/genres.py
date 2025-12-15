from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import GENRES

def genres_keyboard():
    kb = InlineKeyboardBuilder()

    for genre in GENRES:
        kb.button(text=genre.title(), callback_data=f"genre:{genre}")

    kb.adjust(2)
    return kb.as_markup()
