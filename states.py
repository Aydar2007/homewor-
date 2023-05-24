from aiogram.dispatcher.filters.state import State, StatesGroup

class Title(StatesGroup):
    title = State()

class Time(StatesGroup):
    time = State()
class IdMessage(StatesGroup):
    id_message = State()

class Delete(StatesGroup):
    delete = State()