import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import router
from database.sqlite import database_init
from keyboard.set_menu import set_main_menu

logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp['ID_MY_GIRL'] = config.tg_bot.ID_MY_GIRL
    dp['MY_ID'] = config.tg_bot.MY_ID
    dp['mgr'] = config.mgr


    # Регистриуем роутеры в диспетчере
    dp.include_router(router)

    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    # await bot.delete_webhook(drop_pending_updates=True)
    try:
        database_init()
    except:
        logger.error('DATABASE')

    logger.info('Starting bot')

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())