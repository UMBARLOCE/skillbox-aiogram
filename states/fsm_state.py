from aiogram.dispatcher.filters.state import State, StatesGroup


class MyState(StatesGroup):
    price_max = State()  # bestdeal_
    dist_max = State()  # bestdeal_
    city_name = State()
    date_in = State()
    date_out = State()
    hotels_count = State()
    foto_check = State()
    foto_count = State()
    check_find = State()