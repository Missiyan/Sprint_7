import allure
import pytest
import requests

from urls import COURIER_URL, COURIER_LOGIN_URL, BASE_URL
from scripts import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier,
)

@pytest.fixture
def courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    courier_data = {"login": login, "password": password, "firstName": first_name}
    yield courier_data
    with allure.step(f"Удалить курьера {login} после теста"):
        courier_id = login_courier(login, password)
        if courier_id:
            delete_courier(courier_id)

@pytest.fixture
def created_courier_response():     #создаёт курьера и отдаёт (response, login, password)
                                    #register_new_courier_and_return_login_password не возвращает response
                                    # а тесту создания нужен response для проверки 201 и {"ok": true}
                                    # если метод из задания можно менять и  возвращать response
                                    # фикстуры можно объединить
    
    login = "courier_" + __import__("uuid").uuid4().hex[:10]
    payload = {"login": login, "password": "pass", "firstName": "name"}
    response = requests.post(COURIER_URL, data=payload)
    yield response, login, "pass"
    if response.status_code == 201:
        with allure.step(f"Удалить курьера {login} после теста"):
            courier_id = login_courier(login, "pass")
            if courier_id:
                delete_courier(courier_id)