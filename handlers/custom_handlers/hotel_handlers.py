from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from states.fsm_state import MyState
from utils.api_query import global_query
from datetime import datetime
from keyboards.reply.kb_reply import kb_4_commands, kb_city, kb_yes_no
from keyboards.reply.kb_reply import kb_1_2_3_4, kb_3_6_9, kb_50_100_150_200
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery
from database.sq_db import insert_into_query

# data['SortOrder'] = 'PRICE_HIGHEST_FIRST'
# data['SortOrder'] = 'STAR_RATING_HIGHEST_FIRST'
# data['SortOrder'] = 'PRICE'

async def lowprice_(message: types.Message, state: FSMContext) -> None:
    """Дешёвые отели"""
    async with state.proxy() as data:
        data['command']: str = 'lowprice'
        data['sort_hotels']: str = 'PRICE_LOW_TO_HIGH'
        data['filters_hotels']: dict = {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
    await message.answer(text=f'Введите город',
                         reply_markup=kb_city()
                         )
    await MyState.city_name.set()


async def highprice_(message: types.Message, state: FSMContext) -> None:
    """Дорогие отели"""
    async with state.proxy() as data:
        data['command']: str = 'highprice'
        data['sort_hotels']: str = 'PRICE_LOW_TO_HIGH'  # самые дорогие среди первых 200 дешёвых...
        data['filters_hotels']: dict = {"price": {"max": 1_000_000, "min": 500}}  # в диапазоне цен.
    await message.answer(text=f'Введите город',
                         reply_markup=kb_city()
                         )
    await MyState.city_name.set()


async def bestdeal_(message: types.Message, state: FSMContext) -> None:
    """Дешёвые в центре"""
    async with state.proxy() as data:
        data['command']: str = 'bestdeal'
        data['sort_hotels']: str = 'DISTANCE'
    await message.answer(text=f'Введите максимальную цену за ночь',
                         reply_markup=kb_50_100_150_200()
                         )
    await MyState.price_max.set()


async def cancel(message: types.Message, state: FSMContext) -> None:
    """отмена состояния машины состояния"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply(text=f'Запрос отменён.', reply_markup=kb_4_commands())
    await state.finish()


async def price_max(message: types.Message, state: FSMContext) -> None:
    """ловим максимальную цену для /bestdeal"""
    if message.text.isdigit() and int(message.text) > 0:
        async with state.proxy() as data:
            data['filters_hotels']= {"price": {"max": int(message.text), "min": 1}}
        await message.answer(text=f'Введите максимальную удалённость от центра',
                             reply_markup=kb_1_2_3_4()
                             )
        await MyState.dist_max.set()
    else:
        await message.reply(text='Введите натуральное число!', 
                            reply_markup=kb_50_100_150_200()
                            )
        

async def dist_max(message: types.Message, state: FSMContext) -> None:
    """ловим максимальную удалённость для /bestdeal"""
    if message.text.isdigit():
        async with state.proxy() as data:
            data['filters_hotels'] |= {"distance": {"max": int(message.text), "min": 0}}
        await message.answer(text=f'Введите город', reply_markup=kb_city())
        await MyState.city_name.set()
    else:
        await message.reply(text='Введите натуральное число!', 
                            reply_markup=kb_1_2_3_4()
                            )


async def city_name(message: types.Message, state: FSMContext) -> None:
    """ловим название города"""
    async with state.proxy() as data:
        data['city_name']: str = message.text
        data['query_time']: int = int(datetime.now().timestamp())
        data['tg_user_id']: int = message.from_user.id
    await MyState.date_in.set()
    await message.reply(text=f'Введите дату заезда',
                        reply_markup=await DialogCalendar().start_calendar()
                        )


async def date_in(callback_query: CallbackQuery, 
                  callback_data: CallbackData, 
                  state: FSMContext
                  ) -> None:
    """Ловим дату заезда"""
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['date_in']: tuple[int] = (date.year, date.month, date.day)
        await MyState.date_out.set()
        await callback_query.message.answer(
            text=f'Введите дату выезда',
            reply_markup=await DialogCalendar().start_calendar()
            )


async def date_out(callback_query: CallbackQuery, 
                   callback_data: CallbackData, 
                   state: FSMContext
                   ) -> None:
    """Ловим дату выезда и корректное количество дней"""
    selected, date = await DialogCalendar()\
        .process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['date_out']: tuple[int] = (date.year, date.month, date.day)
            date_diff = datetime(*data['date_out']) - datetime(*data['date_in'])
            data['days_count']: int = date_diff.days
        if data['days_count'] > 0:
            await MyState.hotels_count.set()
            await callback_query.message.answer(
                text=f'Сколько отелей ищем?',
                reply_markup=kb_3_6_9()
                )
        else:
            await callback_query.message.answer(
                text='Дата выезда раньше даты заезда.\nВведите корректную дату выезда',
                reply_markup=await DialogCalendar().start_calendar()
                )


async def hotels_count(message: types.Message, state: FSMContext) -> None:
    """ловим необходимое количество отелей"""
    if message.text.isdigit() and int(message.text) > 0:
        async with state.proxy() as data:
            data['hotels_count']: int = int(message.text)
        await message.reply(text=f'Нужны фотки?', reply_markup=kb_yes_no())
        await MyState.foto_check.set()
    else:
        await message.reply(text='Введите натуральное число!', reply_markup=kb_3_6_9())


async def foto_check(message: types.Message, state: FSMContext) -> None:
    """ловим запрос на фото"""
    if message.text == 'Да':
        async with state.proxy() as data:
            data['foto_check']: bool = True
        await message.reply(text='Сколько нужно фоток?', reply_markup=kb_3_6_9())
        await MyState.foto_count.set()
    elif message.text == 'Нет':
        async with state.proxy() as data:
            data['foto_check']: bool = False
            data['foto_count']: int = 0
        await message.reply(text='Начать поиск?', reply_markup=kb_yes_no())
        await MyState.check_find.set()
    else:
        await message.reply(text='Выберите ответ из двух вариантов!', reply_markup=kb_yes_no())


async def foto_count(message: types.Message, state: FSMContext) -> None:
    """ловим необходимое количество фото"""
    if message.text.isdigit():
        async with state.proxy() as data:
            data['foto_count']: int = int(message.text)
        await message.reply(text='Начать поиск?', reply_markup=kb_yes_no())
        await MyState.check_find.set()
    else:
        await message.reply(text='Вы ввели не число!', reply_markup=kb_3_6_9())


async def check_find(message: types.Message, state: FSMContext) -> None:
    """выход из машины состояний, запрос на поиск и сам поиск."""
    if message.text != 'Да':
        await state.finish()
        await message.reply(text='Отмена поиска.', reply_markup=kb_4_commands())
        return
    
    async with state.proxy() as data:
        data['check_find']: bool = True
    await message.reply(text=f'Поиск...', reply_markup=kb_4_commands())
    user_data: dict = await state.get_data()  # берём словарик с данными
    user_data['urls'] = []
    await state.finish()  # выход из машины состояний

    # ЗАПРОСЫ К API
    responce: list[dict] = global_query(**user_data)
    if not responce:
        await message.answer(text="Отели не найдены")
        return

    for hotel_dict in responce:
        for hotel in hotel_dict.values():
            await message.answer(
                f"{hotel['name_hotel']}\n"
                f"Цена за ночь: ${hotel['price_hotel']}\n"
                f"До центра: {hotel['dist_hotel']}\n"
                f"{hotel['address_hotel']}\n"
                f"Дней: {user_data['days_count']}, стоимость: ${user_data['days_count'] * hotel['price_hotel']}\n"
                f"https://www.hotels.com/h{list(hotel_dict.keys())[0]}.Hotel-Information",
                disable_web_page_preview=True
                )
            
            if hotel['photos_hotel']:
                media = []
                for photo in hotel['photos_hotel']:
                    media.append(types.InputMediaPhoto(photo))
                await message.answer_media_group(media=media)
            
            url = f"https://www.hotels.com/h{list(hotel_dict.keys())[0]}.Hotel-Information"
            user_data['urls'].append(url)
    
    await insert_into_query(user_data)  # запись в БД


def reg_hotel_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(lowprice_, commands=['lowprice'], state=None)
    dp.register_message_handler(highprice_, commands=['highprice'], state=None)
    dp.register_message_handler(bestdeal_, commands=['bestdeal'], state=None)
    dp.register_message_handler(cancel, commands=['cancel'], state='*')
    dp.register_message_handler(price_max, state=MyState.price_max)
    dp.register_message_handler(dist_max, state=MyState.dist_max)
    dp.register_message_handler(city_name, state=MyState.city_name)
    dp.register_callback_query_handler(date_in, dialog_cal_callback.filter(), state=MyState.date_in)
    dp.register_callback_query_handler(date_out, dialog_cal_callback.filter(), state=MyState.date_out)
    dp.register_message_handler(hotels_count, state=MyState.hotels_count)
    dp.register_message_handler(foto_check, state=MyState.foto_check)
    dp.register_message_handler(foto_count, state=MyState.foto_count)
    dp.register_message_handler(check_find, state=MyState.check_find)
