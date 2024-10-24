from aiogram.fsm.state import State, StatesGroup

class Cardio(StatesGroup):
    cardio_start    = State()
    type            = State()
    dist            = State()
    date            = State()
    is_competition  = State()
    pay_debt        = State()
    send            = State()

class Climbing(StatesGroup):
    climbing_start    = State()
    type              = State()
    date              = State()
    is_competition    = State()
    send              = State()
