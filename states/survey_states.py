from aiogram.fsm.state import State, StatesGroup

class Cardio(StatesGroup):
    cardio_start = State()
    type = State()
    dist = State()
    is_competition = State()
    pay_debt = State()
