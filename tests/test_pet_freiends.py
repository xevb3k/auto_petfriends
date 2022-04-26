from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, psw=valid_password):
    """
    тест на авторизацию с верными логин/пароль
    :param email: существующий в базе мейл
    :param psw: верный пароль
    :return: код ответа сервера должен быть 200, в ответе должен быть словарь с ключом key
    """
    status, result = pf.get_api_key(email, psw)
    assert status == 200
    assert 'key' in result


def test_get_api_key_invalid_user(email='invalid_email', psw='invalid_password'):
    """
    тест на авторизацию с неверными логин/пароль
    :param email: несуществующий в базе мейл
    :param psw: любой пароль
    :return: код ответа сервера должен быть 403, в ответе не должно быть словаря с ключом key
    """
    status, result = pf.get_api_key(email, psw)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """
    тест запроса на получение списка всех питомцев с валидным ключом
    :param filter: '' - получение всего списка питомцев
    :return: код ответа сервера должен быть 200, в ответе должен быть словарь с ключом "pets",
            по ключу "pets" должен быть список
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pet_list(auth_key, filter)
    assert status == 200
    assert 'pets' in result
    assert type(result['pets']) is list


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """
    тест запроса на получение списка своих питомцев с валидным ключом
    :param filter: 'my_pets' - получение списка только моих питомцев
    :return: код ответа сервера должен быть 200, в ответе должен быть словарь с ключом "pets",
            по ключу "pets" должен быть список
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pet_list(auth_key, filter)
    assert status == 200
    assert 'pets' in result
    assert type(result['pets']) is list


def test_get_my_pets_with_invalid_key(filter='my_pets'):
    """
    тест запроса на получение списка своих питомцев с неверным ключом авторизации
    :param filter: 'my_pets' - получение списка только моих питомцев
    :return: код ответа сервера должен быть 403
    """
    status, result = pf.get_pet_list({'key': 'invalidkey'}, filter)
    assert status == 403

def test_get_all_pets_with_invalid_key(filter=''):
    """
    тест запроса на получение списка всех питомцев с неверным ключом авторизации
    :param filter: '' - получение всего списка питомцев
    :return: код ответа сервера должен быть 403
    """
    status, result = pf.get_pet_list({'key': 'invalidkey'}, filter)
    assert status == 403


# тут баг в API: сервер дает ответ 500 "Internal Server Error" - ошибка для сервера "неожиданная", хотя должна быть ожидаема и может быть обработана
# ответ должен быть 4хх - ошибка пользователя
def test_get_all_pets_with_invalid_key(filter='&^%&$^$()@#'):
    """
    тест запроса на получение списка питомцев с верным ключом авторизации и невалидным значением filter
    :param filter: любое значение кроме '' и 'my_pets'
    :return: код ответа сервера должен быть 4xx
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pet_list(auth_key, filter)
    assert str(status)[0] == '4'


def test_add_new_pet_with_valid_key(name='Бася', animal_type='котя', age='5', pet_photo='images/baks.jpg'):
    """
    тест на добавление нового питомца с фото с валидным ключом и валидными данными питомца
    :param name: имя
    :param animal_type: тип/порода
    :param age: возраст
    :param pet_photo: фото
    :return: код ответа сервера должен быть 200
            в теле ответа должен быть словарь с ключами: age, name, animal_type, значения должны быть равны входным данным
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age


def test_add_new_pet_with_valid_key_empty_data(name='',
                                                 animal_type='',
                                                 age='',
                                                 pet_photo='images/baks.jpg'):
    """
    тест на добавление нового питомца с фото с валидным ключом и пустыми значениями в данных питомца
    :param name: имя
    :param animal_type: тип/порода
    :param age: возраст
    :param pet_photo: фото
    :return: код ответа сервера должен быть 200
            в теле ответа должен быть словарь с ключами: age, name, animal_type, значения должны быть равны входным данным
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age


def test_add_new_pet_with_valid_key_big_data(name='NfCJ!X!cHdrKvXV79Ftke4EkaM&GpAw2ete^#c6t!XjDBT6aYBFny4mHsEToK%ryTzpkkqAgtTgK#%2u&fd2mVrbGmgC$kP2SF@2',
                                                 animal_type='5n3F22RQQoPNhuK9tWHi#THE%Tj#on9MJd8SR^KpN%ngcAVM6jBr&rZqA6ruaSZ&PFe83wW!&u3a8P3ZJ3r8!GeYoRKaTmuc4VRX',
                                                 age='#xFF%DnRWcQ6rjTpHzgF2jMRFPUmHdyHqc8qRf#JzUd5AhYsaiwFzaGwb2osU4iyH9R6YS%Z^JCKAv4v4XWNFVh5sAu$ZFpTd%TH',
                                                 pet_photo='images/baks.jpg'):
    """
    тест на добавление нового питомца с фото с валидным ключом и длинными последовательностями символов в данных
    :param name: имя
    :param animal_type: тип/порода
    :param age: возраст
    :param pet_photo: фото
    :return: код ответа сервера должен быть 200
            в теле ответа должен быть словарь с ключами: age, name, animal_type, значения должны быть равны входным данным
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age


def test_add_new_pet_with_invalid_key(name='Бася', animal_type='котя', age='5', pet_photo='images/baks.jpg'):
    """
    тест на добавление нового питомца с фото с невалидным ключом и валидными данными питомца
    :param name: имя
    :param animal_type: тип/порода
    :param age: возраст
    :param pet_photo: фото
    :return: код ответа сервера должен быть 403
    """
    status, result = pf.add_new_pet({'key': 'invalidkey'}, name, animal_type, age, pet_photo)
    assert status == 403


def test_add_new_pet_simple_with_valid_key(name='Василий', animal_type='котя', age='1'):
    """
    тест на добавление нового питомца без фото с валидным ключом и валидными данными питомца
    :param name: имя
    :param animal_type: тип/порода
    :param age: возраст
    :param pet_photo: фото
    :return: код ответа сервера должен быть 200
            в теле ответа должен быть словарь с ключами: age, name, animal_type, значения должны быть равны входным данным
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age


def test_add_new_pet_simple_with_invalid_key(name='Василий', animal_type='котя', age='1'):
    """
    тест на добавление нового питомца без фото с невалидным ключом и валидными данными питомца
    :param name: имя
    :param animal_type: тип/порода
    :param age: возраст
    :param pet_photo: фото
    :return: код ответа сервера должен быть 403
    """
    status, result = pf.add_new_pet_simple({'key': 'invalidkey'}, name, animal_type, age)
    assert status == 403


def test_del_pet_with_valid_key():
    """
    тест на удаление своих питомцев с валидным ключом
    :return: код ответа сервера должен быть 200
            список питомцев после удаления должен быть пуст
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) == 0:
        raise Exception("Нет питомцев для удаления")
    else:
        for pet in res['pets']:
            status, result = pf.del_pet(auth_key, pet['id'])
            assert status == 200
    _, res = pf.get_pet_list(auth_key, filter='my_pets')
    assert len(res['pets']) == 0


def test_del_pet_with_invalid_key():
    """
    тест на удаление своих питомцев с невалидным ключом
    :return: код ответа сервера должен быть 403
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) == 0:
        raise Exception("Нет питомцев для удаления")
    else:
        for pet in res['pets']:
            status, result = pf.del_pet({'key': 'invalidkey'}, pet['id'])
            assert status == 403


# тут баг - можно удалить чужого питомца со свои ключом!
def test_del_other_pet_with_valid_key():
    """
    тест на удаление чужих питомцев с валидным ключом
    :return: код ответа сервера должен быть 403
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # удалим всех своих
    _, res = pf.get_pet_list(auth_key, filter='my_pets')
    for pet in res['pets']:
        status, result = pf.del_pet(auth_key, pet['id'])

    # пробуем удалить первого из списка не своих
    _, res = pf.get_pet_list(auth_key, filter='')
    status, result = pf.del_pet(auth_key, res['pets'][0]['id'])
    assert status == 403


def test_update_pet_with_valid_key(name='Бася', animal_type='кот', age='10'):
    """
    тест на изменение параметров питомца, с валидным ключом
    :param name: новое имя
    :param animal_type: новый тип
    :param age: новый возраст
    :return: код ответа сервера должен быть 200
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) > 0:
        status, result = pf.update_pet(auth_key, res['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age
    else:
        raise Exception("Нет питомцев для обновления")


def test_update_pet_with_valid_key_big_data(name='NfCJ!X!cHdrKvXV79Ftke4EkaM&GpAw2ete^#c6t!XjDBT6aYBFny4mHsEToK%ryTzpkkqAgtTgK#%2u&fd2mVrbGmgC$kP2SF@2',
                                            animal_type='5n3F22RQQoPNhuK9tWHi#THE%Tj#on9MJd8SR^KpN%ngcAVM6jBr&rZqA6ruaSZ&PFe83wW!&u3a8P3ZJ3r8!GeYoRKaTmuc4VRX',
                                            age='#xFF%DnRWcQ6rjTpHzgF2jMRFPUmHdyHqc8qRf#JzUd5AhYsaiwFzaGwb2osU4iyH9R6YS%Z^JCKAv4v4XWNFVh5sAu$ZFpTd%TH'):
    """
    тест на изменение параметров питомца, с валидным ключом и длинными последовательностями символов в данных
    :param name: новое имя
    :param animal_type: новый тип
    :param age: новый возраст
    :return: код ответа сервера должен быть 200
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) > 0:
        status, result = pf.update_pet(auth_key, res['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age
    else:
        raise Exception("Нет питомцев для обновления")


def test_update_pet_with_invalid_key(name='Бася', animal_type='кот', age='10'):
    """
    тест на изменение параметров питомца, с невалидным ключом
    :param name: новое имя
    :param animal_type: новый тип
    :param age: новый возраст
    :return: код ответа сервера должен быть 403
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) > 0:
        status, result = pf.update_pet({'key': 'invalidkey'}, res['pets'][0]['id'], name, animal_type, age)
        assert status == 403
    else:
        raise Exception("Нет питомцев для обновления")


def test_set_photo_with_valid_key(pet_photo='images/vasya.jpg'):
    """
    тест на добавление/изменение фото питомцу
    :param pet_photo:
    :return: ключ pet_photo должен быть в возвращаемом словаре
            код ответа сервера должен быть 200
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) > 0:
        status, result = pf.set_photo(auth_key, res['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("Нет питомцев для установки фото")


# тут баг в API: сервер дает ответ 500 "Internal Server Error" - ошибка для сервера "неожиданная", хотя должна быть ожидаема и может быть обработана
# ответ должен быть 4хх - ошибка пользователя
def test_set_photo_with_valid_key_invalid_photo(pet_photo='images/excel.xlsx'):
    """
    тест на добавление питомцу фото, вместо фото подложен файл не являющийся изображением
    :param pet_photo:
    :return: ключ pet_photo должен быть в возвращаемом словаре
            код ответа сервера должен быть 4xx
    """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, res = pf.get_pet_list(auth_key, filter='my_pets')

    if len(res['pets']) > 0:
        status, result = pf.set_photo(auth_key, res['pets'][0]['id'], pet_photo)
        assert str(status)[0] == '4'
    else:
        raise Exception("Нет питомцев для установки фото")