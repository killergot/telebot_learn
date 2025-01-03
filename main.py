import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers, wordly, calback, weather
from database.sqlite import db_start


# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp['ID_MY_GIRL'] = config.tg_bot.ID_MY_GIRL
    dp['MY_ID'] = config.tg_bot.MY_ID
    dp['mgr'] = config.mgr


    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(calback.router)
    dp.include_router(wordly.router)
    dp.include_router(weather.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    # await bot.delete_webhook(drop_pending_updates=True)
    try:
        db_start()
    except:
        print('error DATABASE')

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())