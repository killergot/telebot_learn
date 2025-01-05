import random
from copy import deepcopy

from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.database import users_db, user_dict_template
from lexicon.lexicon import LEXICON_RU

from keyboard.keyboard import kb_main
from keyboard.special_keyboard import get_info_kb

router = Router()


@router.message(CommandStart())
async def start_command(message: Message,bot: Bot):
    await bot.send_message(chat_id=message.chat.id,
                            text=LEXICON_RU['/start'],
                            reply_markup=kb_main)
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

@router.message(F.text == 'Привет')
async def sdf(message: Message,state:FSMContext):
    text = str(await state.get_data()) + '\n' + str(await state.get_state())
    await message.answer(text=text,parse_mode=ParseMode.MARKDOWN)

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         parse_mode=ParseMode.HTML)

@router.message(Command(commands='location'))
async def location_command(message: Message,bot:Bot):
    await bot.send_location(chat_id = message.chat.id,
                            latitude = random.random() * 90,
                            longitude = random.random() * 180,
                            reply_markup=kb_main)

@router.message(F.text.lower().startswith('бан'))
async def ban_command(message: Message,bot:Bot):
    await bot.send_photo(chat_id = message.chat.id,
                         photo=('https://sun9-64.userapi.com/impg/mS4p5IfwlNxxWoDCBxv6q3KTIimd-JdpuMw_tw/VaeuwbuY0PM.jpg?size=828x590&quality=95&sign=ad0d39b3d50be3814b435f77518aef1d&type=album'),
                         reply_markup=kb_main)


@router.message(Command(commands='cancel'))
async def cancel_command(message: Message):
    await message.answer('Зачем же в холостую это писать?'
                         'Оно же так ничего не делает...',
                         reply_markup=kb_main)

@router.message(Command(commands='get_info'),F.chat.type == 'private')
async def give_command(message: Message):
    await message.answer(text='Вот несколько специальных кнопок',
                         reply_markup=get_info_kb)

@router.message(Command(commands='get_info'))
async def give_command(message: Message):
    await message.answer(text='Данная команда создана для личных чатов')


