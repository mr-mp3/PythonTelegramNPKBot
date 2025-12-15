from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="🔍 Поиск фильма", callback_data="menu_search")
    kb.button(text="🎯 Фильтры", callback_data="menu_filters")
    kb.button(text="🎲 Случайный фильм", callback_data="menu_random")
    kb.button(text="🏆 Топ фильмов", callback_data="menu_top")

    kb.adjust(2, 2)
    return kb.as_markup()
