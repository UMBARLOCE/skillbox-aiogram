from loader import bot
from aiogram import types
from keyboards.reply.kb_reply import kb_4_commands


async def help_(message: types.Message):
    """Вызвать справку"""
    await bot.send_message(
        message.from_user.id,
        "Бот для поиска оптимальных отелей.\n"
        "Команды с описанием указаны в МЕНЮ.",
        reply_markup=kb_4_commands()
    )
