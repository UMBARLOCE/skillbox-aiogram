from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.sq_db import select_from_query
from datetime import datetime



async def history_(message: types.Message):
    """История поиска"""
    queries: list[tuple[str, int, str]] = await select_from_query(message.from_user.id)
    for query in queries:
        command: str = query[0]
        time = datetime.fromtimestamp(query[1]).strftime('%d.%m.%Y %H:%M')
        urls = '\n'.join(query[2].split(' | '))
        await message.answer(text=
                             f'{command} | '
                             f'{time}\n'
                             f'{urls}',
                             disable_web_page_preview=True
                             )


def reg_history_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(history_, commands=['history'])