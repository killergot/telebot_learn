from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from keyboard.keyboard import kb_main
from lexicon.lexicon import LEXICON_RU
from states.states import basicState


from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Bot,Router
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command(commands=['weather']),StateFilter(default_state))
async def weather_command(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text=LEXICON_RU['weather']['in_city'],
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(basicState.weather)


@router.message(StateFilter(basicState.weather),
                Command(commands='cancel'))
async def cancel_command(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text=LEXICON_RU['weather']['cancel'])

@router.message(StateFilter(basicState.weather))
async def echo_weather(message: Message,bot:Bot, state: FSMContext,mgr):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        text:str=f"""Погода в городе {message.text}:
            {LEXICON_RU['weather']['temp']} {w.temperature('celsius')['temp']},
            {LEXICON_RU['weather']['wind_speed']} {w.wind()['speed']}
            {LEXICON_RU['weather']['detailed_status']} {w.detailed_status}"""
    except:
        await bot.send_message(chat_id=message.chat.id,
                            text='Неверно введен город, попробуйте еще раз!')
    else:
        await bot.send_message(chat_id=message.chat.id,
                            text=text,
                            reply_markup=kb_main)
        await state.clear()



