import requests
import random
import string
from urls import BASE_URL, COURIER_URL, COURIER_LOGIN_URL
import allure

@allure.step("Сгенерировать случайную строку длиной {length}")
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.step("Зарегистрировать нового курьера и вернуть логин/пароль")
def register_new_courier_and_return_login_password():
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(COURIER_URL, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass


@allure.step("Залогинить курьера {login} и вернуть id")
def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(COURIER_LOGIN_URL, data=payload)
    if response.status_code == 200:
        return response.json().get('id')
    return None


@allure.step("Удалить курьера с id={courier_id}")
def delete_courier(courier_id):
    return requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')


@allure.step("Собрать payload заказа с цветом {color}")
def build_order_payload(color):
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2025-06-06",
        "comment": "Sasuke come back to Konoha",
        "color": color,
    }