from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard(show_back: bool = False):
    kb = InlineKeyboardBuilder()

    kb.button(text="🔍 Поиск фильма", callback_data="menu_search")
    kb.button(text="🎯 Фильтры", callback_data="menu_filters")
    kb.button(text="🎲 Случайный фильм", callback_data="menu_random")
    kb.button(text="🏆 Топ фильмов", callback_data="menu_top")

    kb.adjust(2, 2)

    if show_back:
        kb.button(text="⬅ Назад", callback_data="menu_back")
        kb.adjust(2, 2, 1)

    return kb.as_markup()
