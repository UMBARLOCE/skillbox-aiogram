import requests
from config_data.config import headers, base_url


def get_city_id(city_name: str) -> str:
    """id_города, первый из предложенных по API."""
    end_city = 'locations/v3/search'
    querystring = {"q":f"{city_name}","locale":"ru_RU"}

    try:
        response: dict = requests.request(method="GET", url=base_url + end_city,
                                          headers=headers, params=querystring).json()
        city_id = [i['gaiaId'] for i in response['sr'] if i['type'] == 'CITY'][0]
    except Exception as exc:
        print(response)
        return False
    else:
        return city_id


def get_hotels_list(
        date_in: list, date_out: list, city_id: str, hotels_count: int, 
        sort_hotels: str, filters_hotels: dict, command: str, **kwargs
        ) -> list[dict]:
    """Список со словарями отелей."""
    end_list_holels = "properties/v2/list"
    payload = {'currency': 'USD',
            'eapid': 1,
            'locale': 'ru_RU',
            'siteId': 300000001,
            'destination': {'regionId': city_id},
            'checkInDate': {'day': date_in[2], 'month': date_in[1], 'year': date_in[0]},
            'checkOutDate': {'day': date_out[2], 'month': date_out[1], 'year': date_out[0]},
            'rooms': [{'adults': 2}],  # для двух взрослых
            'resultsStartingIndex': 0,  # пагинация, первая страница до 200 элементов на каждой странице
            'resultsSize': 200,  # первая пачка до 200 элементов
            'sort': sort_hotels,
            'filters': filters_hotels
            }
    
    hotels = []  # id, name, dist, price
    try:
        response = requests.request(
            method="POST", url=base_url + end_list_holels, json=payload, headers=headers
            ).json()
        properties = response['data']['propertySearch']['properties']
    except Exception as exc:
        print(response)
        return hotels

    if command == 'highprice':
        # при сортировке от дешевых к дорогим берем пачку в 200 отелей и ...
        # берем срез с конца на количество hotels_count.
        # получается список из самых дорогих отелей среди первых 200 дешевых.
        need_hotels_count = properties[-1:-(hotels_count + 1): -1]
    else:
        need_hotels_count = properties[:hotels_count:]

    for hotel in need_hotels_count:
        try:
            hotels.append({
                hotel['id']: {
                'name_hotel': hotel['name'], 
                'dist_hotel': hotel['destinationInfo']['distanceFromDestination']['value'],
                'price_hotel': int(hotel['price']['lead']['amount'])
                }
            })
        except Exception as exc:
            print(exc, '\nОтели не найдены')
            pass
    return hotels


def get_address_and_photos(id_hotel, set_photo, count_photo) -> dict:
    end_detail = "properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": id_hotel
    }
    try:
        response = requests.request("POST", base_url + end_detail, json=payload, headers=headers).json()
        address_hotel = response['data']['propertyInfo']['summary']['location']['address']['addressLine']
        address_and_photos = {'address_hotel': address_hotel, 'photos_hotel': []}
    except Exception as exc:
        print(response, '\nОшибка с фото и адресом')
        return {'address_hotel': '', 'photos_hotel': []}

    if set_photo:
        gallery = response['data']['propertyInfo']['propertyGallery']['images']
        photos_hotel = {'photos_hotel': [image['image']['url'] for image in gallery][:count_photo]}
        address_and_photos |= photos_hotel
    return address_and_photos


def global_query(date_in, date_out, city_name, hotels_count, foto_check,
                 foto_count, sort_hotels, filters_hotels, command, **kwargs) -> list[dict]:
    """Глобальный запрос, вмещающий в себя запросы выше."""
    id_city = get_city_id(city_name)
    if not id_city:
        return False
    
    list_hotels = get_hotels_list(date_in, date_out, id_city, hotels_count, sort_hotels,
                                  filters_hotels, command)
    if not list_hotels:
        return False
    
    for index, dict_hotel in enumerate(list_hotels):
        for id_hotel in dict_hotel:
            res = get_address_and_photos(id_hotel, foto_check, foto_count)
            list_hotels[index][id_hotel] |= res
    return list_hotels
