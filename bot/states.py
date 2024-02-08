from aiogram.dispatcher.filters.state import State, StatesGroup

class StartState(StatesGroup):
    phone_number_sign_in = State()
    phone_number_sign_up = State()
    name = State()
    birthday = State()

class CahngeProfileState(StatesGroup):
    phone_number = State()
    name = State()
    birthday = State()

class Adm_State(StatesGroup):
    training_date = State()
    megaphone = State()
    text = State()
    photo = State()
    trainings = State()

class Dialogue_State(StatesGroup):
    start = State()