from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboard.keyboard import kb_main
from states.states import basicState

router = Router()

@router.message(StateFilter(default_state),
                Command(commands='give'))
async def give_command(message: Message,bot:Bot,state: FSMContext,ID_MY_GIRL: int):
    if message.from_user.id == ID_MY_GIRL:
        await bot.send_message(chat_id=message.chat.id,
                           text='Введите сообщение, которое хотите передать своему господину: ',
                           reply_markup=ReplyKeyboardRemove())
    else:
         await bot.send_message( chat_id=message.chat.id,
                           text='Введите сообщение, которое хотите передать своей коллеге по сексу: ',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(basicState.broadcast)


@router.message(StateFilter(basicState.broadcast),
                Command(commands='cancel'))
async def cansel(message: Message,
                 state: FSMContext):
    await message.answer(text='Ну ладно, не будем ничего отправлять',
                         reply_markup=kb_main)
    await state.set_state(default_state)

@router.message(StateFilter(basicState.broadcast))
async def broadcast_command(message: Message,bot:Bot, state: FSMContext,ID_MY_GIRL,MY_ID):
    try:
        temp_chat_id = MY_ID if message.from_user.id == ID_MY_GIRL else ID_MY_GIRL
        await message.send_copy(chat_id=temp_chat_id)
        await bot.send_message(chat_id=message.chat.id,
                               text='Передано успешно',
                               reply_markup=kb_main)
        await state.clear()
    except:
        await bot.send_message(chat_id=message.chat.id,
                               text='Произошла ошибка, поменяй что-то и пробуй еще раз')
