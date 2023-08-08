from loader import bot
from aiogram import types
from keyboards.reply.kb_reply import kb_4_commands


async def start_(message: types.Message):
    """Запустить бота"""
    await bot.send_message(
        message.from_user.id,
        f"Привет, {message.from_user.full_name}!",
        reply_markup=kb_4_commands()
    )
