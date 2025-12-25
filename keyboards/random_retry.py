from aiogram.utils.keyboard import InlineKeyboardBuilder

def random_retry_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔁 Попробовать ещё раз", callback_data="random_retry")
    kb.button(text="⬅ Назад", callback_data="menu_back")
    kb.adjust(1)
    return kb.as_markup()
