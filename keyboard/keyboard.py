from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

kb_main = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text='/game'),
        KeyboardButton(text='/help'),
        KeyboardButton(text='/photo')],[KeyboardButton(text='/location'),
        KeyboardButton(text='/give'),
        KeyboardButton(text='/weather')]],
        resize_keyboard=True
)

kb_game_main_bun = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text='Угадываем'),
        KeyboardButton(text='Загадать Господину')],
        [KeyboardButton(text='/cancel')]],
        resize_keyboard=True
)

kb_game_main = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text='Угадываем'),
        KeyboardButton(text='Загадать Клубничке')],
        [KeyboardButton(text='/cancel')]],
        resize_keyboard=True
)

kb_game_confirm = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text='Все верно'),
        KeyboardButton(text='Поменяем')],
        [KeyboardButton(text='/cancel')]],
        resize_keyboard=True
)

ikb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='❤️',callback_data='like'),
        InlineKeyboardButton(text='👎🏾',callback_data='dislike')],
                     [InlineKeyboardButton(text='Другое фото',callback_data='Другое фото')],
                     [InlineKeyboardButton(text='Главное меню',callback_data='Главное меню')]])

def create_inline_kb(tempStr : str) -> InlineKeyboardMarkup:
    keyboard : list[list[InlineKeyboardButton]] = [[],[],[],[],[]]
    counter = 1
    for i in tempStr:
        keyboard[counter // 8].append(InlineKeyboardButton(text=i,callback_data='for_wordly'))
        counter+=1

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
