from aiogram.utils import executor
from aiogram import Dispatcher
from loader import dp
from utils.reg_commands import reg_handlers, set_commands
from database.sq_db import create_table


async def on_startup(_):
    """Запускается один раз при включении бота."""
    create_table()
    reg_handlers(dp)
    await set_commands(dp)
    print('Бот он-лайн')


async def on_shutdown(dp: Dispatcher):
    """Запускается один раз при выключении бота."""
    await dp.storage.close()
    await dp.storage.wait_closed()
    print("Бот офф-лайн")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           )
