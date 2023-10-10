import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


# метод __init__ используется для установки начальных значений атрибутов объектов,
# которые будут создаваться в этом классе. base_url - это атрибут
class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'


    # Метод для получения аутентификационного ключа, МЫ определяем названия переменных
    # Для передачи данных в заголовке, создаётся словарь headers
    # в кавычках - это точное название из документации, после : наши переменные
    def get_api_key(self, email: str, password: str) -> json:
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальным
        ключом пользователя, найденным по указанным email и password'''

        headers = {
            'email': email,
            'password': password
        }

        # отправляем GET-запрос
        # создаём переменную responce для записи в неё ответа от сервера
        # get - тип запроса из документации, url - из документации,
        # первый headers - это "ключевое слово", второй headers - это наш словарь
        responce = requests.get(self.base_url + '/api/key', headers = headers)

        # status - переменная для сохранения статус-кода из ответа от сервера
        # result = ""  - объявляем переменную для сохранения ответа от сервера
        status = responce.status_code
        result = ""

        # присваиваем переменной result ответ от сервера в формате json
        # на случай, если json извлечь не получилось, выведем в виде текста
        # return используется для завершения работы функции/метода и возвращает указанные данные туда,
        # где функция/метод вызывается
        # исключение JSONDecodeError возникает при невозможности декодировать ответ в JSON формат. Можно оставить блок
        # except пустым, но лучше указать конкретный тип исключения
        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON со списком
        найденных питомцев, совпадающих с фильтром. Фильтр может иметь пустое значение - получить список всех
        питомцев, либо my_pets - получить список собственных питомцев'''

        headers = {'auth_key': auth_key['key']}

        # по документации фильтр передаётся НЕ в заголовке, а в query
        filter = {'filter': filter}

        responce = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text

        print(result)
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        '''Метод делает POST запрос к API сервера на добавление нового питомца и возвращает статус запроса и
        результат в формате JSON с данными о добавленном питомце.'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        responce = requests.post(self.base_url + '/api/pets', headers=headers, data=data)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text

        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер DELETE запрос на удаление питомца по id и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        responce = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text

        print(status, result)
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет PUT запрос на сервер об обновлении данных питомца по указанному id и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        responce = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text

        print(result)
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет POST запрос на сервер, который добавляет фотографию к уже созданному питомцу по
        его id и возвращает статус запроса и result в формате JSON с обновлёнными данными"""

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        responce = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, files=file)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
            result['pet_photo'] = pet_photo # Добавляем ключ 'pet_photo' со значением pet_photo в результат
        except json.decoder.JSONDecodeError:
            result = responce.text
        print(status)
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        '''Метод делает POST запрос к API сервера на добавление нового питомца без фото, возвращает статус
        запроса и результат в формате JSON с данными о питомце.'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        responce = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text

        return status, result