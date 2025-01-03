from aiogram.fsm.state import StatesGroup, State

class gameState(StatesGroup):
    menu = State()
    preChoise = State()
    choise = State()
    confirm = State()
    inGame = State()

class basicState(StatesGroup):
    weather = State()
    broadcast = State()
    add_photo = State()
