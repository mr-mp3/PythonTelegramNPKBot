from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.states import FilterStates
from services.database import save_filters, reset_filters

router = Router()


@router.callback_query(F.data == "filter_year")
async def filter_year(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("📅 Введите минимальный год (1900–2025):")
    await state.set_state(FilterStates.year)
    await call.answer()


@router.callback_query(F.data == "filter_rating")
async def filter_rating(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("⭐ Введите минимальный рейтинг (0–10):")
    await state.set_state(FilterStates.rating)
    await call.answer()


@router.message(FilterStates.year)
async def process_year(message: Message, state: FSMContext):
    try:
        year = int(message.text)
        if year < 1900 or year > 2025:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введите год от 1900 до 2025")
        return

    await state.update_data(year=year)
    await message.answer("⭐ Теперь введите минимальный рейтинг (0–10):")
    await state.set_state(FilterStates.rating)


@router.message(FilterStates.rating)
async def process_rating(message: Message, state: FSMContext):
    try:
        rating = float(message.text)
        if rating < 0 or rating > 10:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введите число от 0 до 10")
        return

    data = await state.get_data()
    save_filters(message.from_user.id, data.get("year"), rating)

    await state.clear()
    await message.answer(
        f"✅ Фильтры сохранены:\n"
        f"📅 Год ≥ {data.get('year')}\n"
        f"⭐ Рейтинг ≥ {rating}"
    )


@router.callback_query(F.data == "filter_reset")
async def reset_filters_handler(call: CallbackQuery):
    reset_filters(call.from_user.id)
    await call.message.edit_text("♻️ Фильтры сброшены")
    await call.answer()
