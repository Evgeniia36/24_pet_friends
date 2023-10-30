import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'


    def get_api_key(self, email: str, password: str) -> json:
        '''The method sends a request to the server's API and returns the request status and the result in JSON format
        with a unique user key found using the specified email and password'''

        headers = {
            'email': email,
            'password': password
        }

        responce = requests.get(self.base_url + '/api/key', headers = headers)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        '''The method sends a request to the server's API and returns the request status and the result in JSON format,
        including a list of found pets that match the filter. The filter can have an empty value to get a list of all pets
        or 'my_pets' to get a list of a user's own pets.'''

        headers = {'auth_key': auth_key['key']}

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
        '''The method sends a POST request to the server's API to add a new pet and returns the request status and the result
        in JSON format with information about the added pet.'''

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
        """The method sends a DELETE request to the server to remove a pet by ID and returns the request status and the result
        in JSON format with a success notification message. Currently, there is a bug where the 'result' field receives an empty string,
        but the 'status' is still 200"""

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
        """The method sends a PUT request to the server to update pet data based on the specified ID and returns the request status
        and 'result' in JSON format with the updated pet data."""

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
        """The method sends a POST request to the server to add a photo to an already created pet based on its ID
        and returns the request status and 'result' in JSON format with the updated data"""

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        responce = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, files=file)

        status = responce.status_code
        result = ""

        try:
            result = responce.json()
        except json.decoder.JSONDecodeError:
            result = responce.text
        print(status)
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        '''The method sends a POST request to the server's API to add a new pet without a photo and returns the request status
        and the result in JSON format with pet data.'''

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
