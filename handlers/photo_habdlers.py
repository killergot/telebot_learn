from asyncio import sleep

from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto

from database.sqlite_photo import get_random_photo, create_photo, delete_photo
from keyboard.keyboard import kb_main, ikb
from lexicon.lexicon import LEXICON_RU
from states.states import PhotoState

router = Router()

@router.message(Command(commands='add_photo'))
async def add_photo(message: Message,bot:Bot,state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                            text=LEXICON_RU['/add_photo'],
                            reply_markup=ReplyKeyboardRemove())
    await state.set_state(PhotoState.add_photo)

@router.message(StateFilter(PhotoState.add_photo),F.photo)
async def add_photo_continue(message: Message,
                    bot:Bot,
                    state: FSMContext,
                    db):
    photo = message.photo[-1].file_id
    response_create = await create_photo(photo,db)
    await bot.send_message(chat_id=message.chat.id,
                           text=response_create,
                           reply_markup=kb_main)
    await state.clear()

@router.message(StateFilter(PhotoState.add_photo))
async def add_photo_warning(message: Message,bot:Bot):
    await bot.send_message(chat_id=message.chat.id,
                           text=LEXICON_RU['/add_photo_warning'])

@router.message(Command(commands=['photo']),StateFilter(default_state))
async def get_photo(message: Message,
                            bot:Bot,
                            state: FSMContext,
                            db):
    monke = await get_random_photo('1',db)
    if monke:
        await state.update_data({'monke': monke})
        sent_message = await message.answer('Можете удалить, а можете оставить?',
                             reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        # Возможно буду потом удалять сообщения при выходе из состояния
        await bot.send_photo(chat_id = message.chat.id,
                            photo=monke,
                            caption='Вот обезьянка',
                            reply_markup=ikb)
        await state.set_state(PhotoState.get_photo)
        await sleep(5)
        await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=LEXICON_RU['not_found_photo'],)

get_photo_router = Router()
get_photo_router.message.filter(StateFilter(PhotoState.get_photo))
get_photo_router.callback_query.filter(StateFilter(PhotoState.get_photo))

@get_photo_router.callback_query(F.data == 'like')
async def callback_photo_like(callback: CallbackQuery):
    await callback.answer(text='Супер')


@get_photo_router.callback_query(F.data == 'dislike')
async def callback_photo_dislike(callback: CallbackQuery,
                                  state: FSMContext,
                                  db):
    monke = await state.get_data()
    monke = monke['monke']
    await callback.answer(text=await delete_photo(monke,db))

@get_photo_router.callback_query(F.data == 'Другое фото')
async def callback_photo_another(callback: CallbackQuery,
                                  state: FSMContext,
                                  db):
    monke = await state.get_data()
    new_monke = await get_random_photo(monke['monke'],db)
    if new_monke:
        await callback.message.edit_media(InputMediaPhoto(media=new_monke,
                                                           type='photo',
                                                           caption='Вот другая обезьянка'),
                                          reply_markup=ikb)
        await state.update_data({'monke': new_monke})
    else:
        await callback.answer(text=LEXICON_RU['one_photo'])

@get_photo_router.callback_query()
async def callback_photo_(callback: CallbackQuery,
                          bot: Bot,
                                  state: FSMContext):
    await callback.message.answer(text = 'Вы вернулись в главное меню',
                                  reply_markup=kb_main)
    temp = await state.get_state()
    await bot.send_message(chat_id=callback.message.chat.id,
                           text=str(temp))
    await callback.message.delete()
    await callback.answer()
    await state.clear()


router.include_router(get_photo_router)

@router.callback_query(F.data.in_(['like',
                                   'dislike',
                                   'Другое фото',
                                   'Главное меню']),
                       StateFilter(default_state))
async def callback_photo_without_state(callback: CallbackQuery):
    await callback.answer(text='Эти кнопки не для вас!')

@router.message(or_f(StateFilter(PhotoState.get_photo),
                       StateFilter(PhotoState.add_photo)),
                Command(commands='cancel'))
async def photo_photo(message: Message,
                               state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel_photo'],)
    await state.clear()

@router.message(StateFilter(PhotoState.get_photo))
async def photo_photo(message: Message,
                      bot:Bot):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
