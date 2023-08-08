from aiogram.types import ReplyKeyboardMarkup


def kb_4_commands() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('/lowprice', '/highprice')
    kb.row('/bestdeal', '/history')
    return kb


def kb_city() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('Лондон', 'Париж', 'Рим')
    kb.row('/cancel')
    return kb


def kb_3_6_9() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('3', '6', '9')
    kb.row('/cancel')
    return kb


def kb_yes_no() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('Да', 'Нет')
    kb.row('/cancel')
    return kb


def kb_50_100_150_200() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('50', '100', '150', '200')
    kb.row('/cancel')
    return kb


def kb_1_2_3_4() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('1', '2', '3', '4')
    kb.row('/cancel')
    return kb