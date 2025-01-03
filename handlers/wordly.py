from distutils.dist import command_re

from aiogram import types, Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.states import gameState
from aiogram.filters import Command

import pymorphy3

from keyboard.keyboard import kb_main,create_inline_kb,kb_game_main,kb_game_main_bun,kb_game_confirm

morph = pymorphy3.MorphAnalyzer()

wordForBun: str = 'панда'
wordForSir: str = 'карта'
tempWord = [[], [], [], [], [], []]
tempWordCounter = dict()

counter: int = 0

router = Router()



@router.message(Command(commands=['game']))
async def game_command(message: types.Message, bot: Bot, state: FSMContext,ID_MY_GIRL):
    await state.set_state(gameState.menu)
    if (message.from_user.id == ID_MY_GIRL):
        keyboard = kb_game_main_bun
    else:
        keyboard = kb_game_main
    await bot.send_message(chat_id=message.chat.id,
                           text='В этой игре вам нужно отгадать слово за 6 попыток.\n'
                                'Вы хотите загадать слово или отгадывать?',
                           reply_markup=keyboard)


@router.message(gameState.menu,F.text.startswith('Загадать'))
async def menu_command(message: types.Message, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text='Какое слово хотите загадать?',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(gameState.choice)


@router.message(gameState.choise)
async def game_choise(message: types.Message, bot: Bot, state: FSMContext,ID_MY_GIRL):
    global wordForSir, wordForBun
    if message.from_user.id == ID_MY_GIRL:
        wordForSir = message.text.lower()
    else:
        wordForBun = message.text.lower()

    await bot.send_message(chat_id=message.chat.id,
                           text=f'Ваше слово: {message.text}\nВсе верно?',
                           reply_markup=kb_game_confirm)

    await state.set_state(gameState.confirm)

@router.message(gameState.confirm)
async def game_confirm(message: types.Message, bot: Bot, state: FSMContext):
    if message.text == 'Все верно':
        await bot.send_message(chat_id=message.chat.id,
                               text='Слово загруженно',
                               reply_markup=kb_main)
        await state.clear()
    elif message.text == 'Поменяем':
        await state.set_state(gameState.choice)
        await bot.send_message(chat_id=message.chat.id,
                               text='Введите новое слово: ',
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Нет такого варианта',
                               reply_markup=kb_game_confirm)


wordForGame = ''

@router.message(gameState.menu,F.text=='Угадываем')
async def check_word(message: types.Message, bot: Bot, state: FSMContext,ID_MY_GIRL):
    wordForBun
    wordForSir
    global wordForGame
    if message.from_user.id == ID_MY_GIRL:
        wordForGame = wordForBun
    else:
        wordForGame = wordForSir

    if wordForGame != '':
        for j in range(0, 6):
            for i in range(0, len(wordForGame)):
                tempWord[j].append('_')

        temp = ' '.join(tempWord[0])
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Вам загадали слово длинной {temp} {len(tempWord[0])} букв\n'
                                    'Попробуйте угадать его!')
        await state.set_state(gameState.inGame)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Вам еще не загадали слово')


counter = 0
full_kb = 'йёцукенгшщзхъфывапролджэячсмитьбю'


@router.message(gameState.inGame)
async def start_game(message: types.Message, bot: Bot, state: FSMContext):
    tempWordCounter = dict()
    wordForGame
    global tempWord
    global full_kb
    inputText = message.text.lower()
    for i in wordForGame:
        if i in tempWordCounter:
            tempWordCounter[i] += 1
        else:
            tempWordCounter[i] = 1
    if len(inputText) == len(tempWord[0]):
        count = 0
        x = morph.parse(inputText)
        for i in x:
            if 'NOUN' in i.tag and inputText == i.normal_form and morph.word_is_known(inputText):
                if not ('Geox' in i.tag or 'Name' in i.tag) and i.score > 0.1:
                    count = 1
        if not count:
            await message.answer(text=f'Слово <code>{inputText}</code> не разрешено!',
                                 parse_mode=ParseMode.HTML)
            return
        global counter
        on_print: str = ''
        for i in range(len(tempWord[counter])):
            if inputText[i] == wordForGame[i]:  # если буква на своем месте
                tempWord[counter][i] = '<b><code>' + inputText[i] + '</code></b>'
                tempWordCounter[inputText[i]] -= 1

        for i in range(len(tempWord[counter])):
            if tempWord[counter][i] == '_':
                if inputText[i] in tempWordCounter:  # если буква есть, но не на своем месте
                    if tempWordCounter[inputText[i]] > 0:
                        tempWord[counter][i] = '<u>' + inputText[i] + '</u>'
                        tempWordCounter[inputText[i]] -= 1
                    else:  # если буква есть, но уже лишний раз
                        tempWord[counter][i] = '<strike>' + inputText[i] + '</strike>'
                else:  # если буквы вообще нет
                    tempWord[counter][i] = '<strike>' + inputText[i] + '</strike>'
                    if inputText[i] in full_kb:
                        x = full_kb.find(inputText[i])
                        full_kb = full_kb[:x] + full_kb[x + 1:]
        counter += 1
        for j in tempWord:
            a = '   '.join(j)
            on_print += a + '\n'
        await bot.send_message(chat_id=message.chat.id,
                               text=f'{on_print}',
                               parse_mode=ParseMode.HTML,
                               reply_markup=create_inline_kb(full_kb))
        if message.text.lower() == wordForGame:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Вы угадали слово с {counter} попытки!',
                                   reply_markup=kb_main)
            await state.clear()
            full_kb = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
            tempWord = [[], [], [], [], [], []]
            counter = 0
        elif counter == 6:
            tempWord = [[], [], [], [], [], []]
            counter = 0
            full_kb = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Вы не угадали слово!!\n'
                                        f'Ваше слово: {wordForGame}',
                                   reply_markup=kb_main)
    else:
        await message.answer('Не может быть слово другой длины, попробуйте снова')