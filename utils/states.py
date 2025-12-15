from aiogram.fsm.state import State, StatesGroup

class FilterStates(StatesGroup):
    year = State()
    rating = State()

class SearchStates(StatesGroup):
    waiting_for_query = State()
