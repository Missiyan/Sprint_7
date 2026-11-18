import pytest
import requests
from scripts import BASE_URL, register_new_courier_and_return_login_password, login_courier, delete_courier

@pytest.fixture
def courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    courier_data = {"login": login, "password": password, "firstName": first_name}
    yield courier_data
    # удаляем курьера
    courier_id = login_courier(login, password)
    if courier_id:
        delete_courier(courier_id)