from aiogram import Router
from aiogram.types import CallbackQuery, InputMediaPhoto

from database.sqlite import delete_photo, get_random_photo
from keyboard.keyboard import ikb, kb_main
from states.states import gameState
from handlers.user_handlers import monke

router = Router()


@router.callback_query(gameState.inGame)
async def basic_callback(callback: CallbackQuery):
    await callback.answer(text='Это просто буква, не тыкай')


@router.callback_query()
async def photo_callback(callback: CallbackQuery):
    global monke # это очень плохо!!!!
    if callback.data == 'like':
        await callback.answer(text='Супер')
    elif callback.data == 'dislike':
        await callback.answer(text=await delete_photo(monke))
    elif callback.data == 'Другое фото':
        new_monke = await get_random_photo()
        while monke == new_monke:
            new_monke = await get_random_photo()
        monke=new_monke
        await callback.message.edit_media(InputMediaPhoto(media=monke,
                                                           type='photo',
                                                           caption='Вот другая обезьянка'),
                                          reply_markup=ikb)
        await callback.answer()
    else :
        await callback.message.answer(text = 'Вы вернулись в главное меню',
                                      reply_markup=kb_main)
        await callback.message.delete()
        await callback.answer()
