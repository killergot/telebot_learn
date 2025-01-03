LEXICON_RU: dict[str, str] = {
    '/start': 'Салам пополам плебей. Не знаешь что делать? '
              'Тыкай на /help',
    '/help': """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>начинает работу бота</em>
<b>/photo</b> - <em>отправляет картинку</em>
<b>/location</b> - <em>отправляет локацию</em>
<b>/give</b> - <em>Передачка сообщений</em>
<b>/weather</b> - <em>Показывает погоду</em>
<b>/game</b> - <em>Игра в угадывание слов</em>
<b>/links</b> - <em>Позволяет добавить фото</em>
<b>/cancel</b> - <em>Отменяет любое действие</em>
    """,
    'no_echo': 'Не получается повторить..',
    'send_photo': 'Отправьте фотографию',
    'weather':{
        'weather_in_city': '',
        'temp': 'Температура:',
        'wind_speed': 'Cкорость ветра:',
        'detailed_status': 'В данном городе сейчас'
    }
}