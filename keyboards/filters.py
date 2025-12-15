from aiogram.utils.keyboard import InlineKeyboardBuilder

def filters_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="📅 Задать год", callback_data="filter_year")
    kb.button(text="⭐ Задать рейтинг", callback_data="filter_rating")
    kb.button(text="❌ Сбросить фильтры", callback_data="filter_reset")

    kb.adjust(1)
    return kb.as_markup()
