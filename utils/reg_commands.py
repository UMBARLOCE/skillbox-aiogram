from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from handlers.default_handlers import start, help, echo
from handlers.custom_handlers import hotel_handlers, history


def reg_handlers(dp: Dispatcher):
    """Регистрация хендлеров"""
    hotel_handlers.reg_hotel_handlers(dp)
    history.reg_history_handlers(dp)
    # start.start_(dp)
    # help.help_(dp)
    dp.register_message_handler(start.start_, commands=['start'])
    dp.register_message_handler(help.help_, commands=['help'])
    # all_commands = [start.start_, help.help_]
    # [
    #     dp.register_message_handler(func, commands=func.__name__[:-1])
    #     for func in all_commands
    #     ]
    dp.register_message_handler(echo.echo_)  # эхо последнее


async def set_commands(dp: Dispatcher):
    """Регистрация команд с подсказками в меню бота."""
    all_commands = [
        hotel_handlers.lowprice_,
        hotel_handlers.highprice_,
        hotel_handlers.bestdeal_,
        history.history_,
        start.start_,
        help.help_,
        ]

    await dp.bot.set_my_commands([
        BotCommand(command=f"/{func.__name__[:-1]}", description=func.__doc__)
        for func in all_commands
        ])
