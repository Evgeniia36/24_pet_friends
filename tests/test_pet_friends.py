import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список. Для этого сначала получаем
    api ключ и сохраняем в переменную auth_key. Далее, используя этого ключ запрашиваем список всех
    питомцев и проверяем что список не пустой. Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Bella', animal_type='zebra', age='8', pet_photo='images/zebra.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_own_pet():
    """Проверяем возможность удаления своего питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Bella', 'zebra', 8, 'images/zebra.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_own_pet_info(name='Bob', animal_type='dog', age=5):
    '''Проверяем возможность обновления информации о питомце из своего списка'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить имя, тип и возраст первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')

def test_successful_add_new_simple_pet(name='Bella', animal_type='zebra', age='8'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_successful_add_photo_of_pet(pet_photo = 'images/zebra.jpg'):
    """Проверяем возможность добавить фото к своему существующему питомцу"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить фото первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception('There is no my pets')

# Далее негативные сценарии

def test_unsuccessful_get_api_key_invalid_email(email='invalid@email.ru', password=valid_password):
    """ Проверяем что запрос api ключа с некорректным email возвращает статус 403 Forbidden"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_unsuccessful_get_api_key_invalid_password(email=valid_email, password='invalid_password'):
    """ Проверяем что запрос api ключа с некорректным паролем возвращает статус 403 Forbidden"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_unsuccessful_get_api_key_empty_email(email='', password=valid_password):
    """ Проверяем что запрос api ключа с пустым значением email возвращает статус 403 Forbidden"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_unsuccessful_get_api_key_empty_password(email=valid_email, password=''):
    """ Проверяем что запрос api ключа с пустым значением пароля возвращает статус 403 Forbidden"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_unsuccessful_delete_not_own_pet(): # БАГ - можно удалить чужого питомца
    """Проверяем НЕвозможность удаления не своего питомца"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Проверяем - если список питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
    if len(all_pets['pets']) == 0:
        raise Exception('There is no pets')
    else:
        pet_id = all_pets['pets'][0]['id'] # Берём id первого питомца из списка и отправляем запрос на удаление
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Проверяем что статус ответа 403 Forbidden
        assert status == 403

def test_unsuccessful_update_not_own_pet_info(name='Bom', animal_type='dog', age=3): # БАГ - можно изменить данные чужого питомца
    '''Проверяем НЕвозможность обновления информации о чужом питомце'''

    # Получаем ключ auth_key и список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
    if len(all_pets['pets']) == 0:
        raise Exception('There is no pets')
    # Если список не пустой, то пробуем обновить имя, тип и возраст первого питомца
    else:
        status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа 403 Forbidden
        assert status == 403

def test_unsuccessful_add_new_simple_pet_empty_fields(name='', animal_type='', age=''): # БАГ - можно добавить питомца с пустыми полями
    """Проверяем что нельзя добавить питомца с незаполненными полями"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа 400 Bad Request
    assert status == 400

def test_unsuccessful_add_new_simple_pet_long_name(name='Че№#"*%,:!?витиесоциал3456ьноэкономическоffdечтотретьеfsdfdsvг\
оданн456ымистраныценностейнеобходимостьнашейноМираоценитьсчегоихиззачастностиростнетчастностиразвитияТретьегоростс\
траныпоэтапногодоценностейморальныхСмешанынашейсомненийобществасростихактивностиоИколи', animal_type='cat', age='1'):
    """Проверяем что нельзя добавить питомца со слишком длинным именем"""
    # БАГ - можно добавить питомца с очень длинным именем + поле name принимает спец-символы

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа 400 Bad Request
    assert status == 400

def test_unsuccessful_add_new_simple_pet_simbols_in_age(name='Goga', animal_type='fixus', age='аb%,ö'):
    """Проверяем что нельзя добавить питомца с буквами/символами в поле возраст"""
    # БАГ - поле возраст принимает любые значения

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа 400 Bad Request
    assert status == 400
