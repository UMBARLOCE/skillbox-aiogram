from loader import bot
from aiogram import types
from keyboards.reply.kb_reply import kb_4_commands


async def echo_(message: types.Message):
    """Пустой хендлер"""
    await bot.send_message(
        message.from_user.id,
        f"Эхо без состояния или фильтра.\nСообщение: {message.text}",
        reply_markup=kb_4_commands()
    )
