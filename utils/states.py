from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    phone = State()
    app_choice = State()
    about = State()
    verified = State()
    speaking_link = State()
