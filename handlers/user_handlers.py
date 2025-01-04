import random

from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database.sqlite import create_photo, get_random_photo
from lexicon.lexicon import LEXICON_RU

from keyboard.keyboard import kb_main, ikb
from keyboard.special_keyboard import get_info_kb
from states.states import basicState

router = Router()
monke : str = '1'


@router.message(CommandStart())
async def start_command(message: Message,bot: Bot):
    await bot.send_message(chat_id=message.chat.id,
                            text=LEXICON_RU['/start'],
                            reply_markup=kb_main)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         parse_mode=ParseMode.HTML)

@router.message(Command(commands='links'))
async def links_command(message: Message,bot:Bot,state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                            text=LEXICON_RU['send_photo'],
                            reply_markup=ReplyKeyboardRemove())
    await state.set_state(basicState.add_photo)

@router.message(Command(commands='location'))
async def location_command(message: Message,bot:Bot):
    await bot.send_location(chat_id = message.chat.id,
                            latitude = random.random() * 90,
                            longitude = random.random() * 180,
                            reply_markup=kb_main)


@router.message(basicState.add_photo)
async def add_photo(message: Message,bot:Bot,state: FSMContext):
    photo = message.photo[-1].file_id
    response_create = await create_photo(photo)
    await bot.send_message(chat_id=message.chat.id,
                           text=response_create,
                           reply_markup=kb_main)
    await state.clear()

@router.message(Command(commands=['photo']))
async def get_photo_command(message: Message,bot:Bot):
    global monke
    monke = await get_random_photo()
    await message.answer('Удалить или оставить?',
                         reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id = message.chat.id,
                        photo=monke,
                        caption='Вот обезьянка',
                        reply_markup=ikb)

@router.message(F.text.lower().startswith('бан'))
async def ban_command(message: Message,bot:Bot):
    await bot.send_photo(chat_id = message.chat.id,
                         photo=('https://sun9-64.userapi.com/impg/mS4p5IfwlNxxWoDCBxv6q3KTIimd-JdpuMw_tw/VaeuwbuY0PM.jpg?size=828x590&quality=95&sign=ad0d39b3d50be3814b435f77518aef1d&type=album'),
                         reply_markup=kb_main)


@router.message(Command(commands='cancel'))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие успешно отменено (даже если никакого действия не было, кто-то все отменил!!!)',
                         reply_markup=kb_main)
    global tempWord
    global counter
    tempWord = [[], [], [], [], [], []]
    counter = 0

@router.message(Command(commands='give'))
async def give_command(message: Message,bot:Bot,state: FSMContext,ID_MY_GIRL):
    if message.from_user.id == ID_MY_GIRL:
        await bot.send_message(chat_id=message.chat.id,
                           text='Введите сообщение, которое хотите передать своему господину: ',
                           reply_markup=ReplyKeyboardRemove())
    else:
         await bot.send_message( chat_id=message.chat.id,
                           text='Введите сообщение, которое хотите передать своей коллеге по сексу: ',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(basicState.broadcast)

@router.message(Command(commands='get_info'),F.chat.type == 'private')
async def give_command(message: Message):
    await message.answer(text='Вот несколько специальных кнопок',
                         reply_markup=get_info_kb)

@router.message(Command(commands='get_info'))
async def give_command(message: Message):
    await message.answer(text='Данная команда создана для личных чатов')


@router.message(basicState.broadcast)
async def broadcast_command(message: Message,bot:Bot, state: FSMContext,ID_MY_GIRL,MY_ID):
    if message.from_user.id == ID_MY_GIRL:
        try:
            await message.send_copy(chat_id=MY_ID)
            await bot.send_message(chat_id=message.chat.id,
                                   text='Передано успешно',
                                   reply_markup=kb_main)
            await state.clear()
        except:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Произошла ошибка, поменяй что-то и пробуй еще раз')
    else:
        try:
            await message.send_copy(chat_id=ID_MY_GIRL)
            await bot.send_message(chat_id=message.chat.id,
                                   text='Передано успешно',
                                   reply_markup=kb_main)
            await state.clear()
        except:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Произошла ошибка, поменяй что-то и пробуй еще раз')
