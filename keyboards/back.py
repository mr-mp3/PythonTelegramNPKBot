from aiogram.utils.keyboard import InlineKeyboardBuilder

def back_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅ Назад", callback_data="menu_back")
    return kb.as_markup()