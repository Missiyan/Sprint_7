import allure
import pytest
import requests
from urls import COURIER_URL
from data import (
    COURIER_CREATE_MIS_FIELD_TEXT,
    COURIER_DUPLICATE_LOGIN_TEXT,
    STATUS_CREATED,
    STATUS_BAD_REQUEST,
    STATUS_CONFLICT,
)

@allure.feature("Курьер")
@allure.story("Создание курьера")
class TestCourierCreation:

    @allure.title("Создание курьера - успех")
    def test_create_courier_success(self, created_courier_response):
        response, login, password = created_courier_response

        with allure.step("Проверить код 201 и тело {'ok': true}"):
            assert response.status_code == STATUS_CREATED
            assert response.json() == {"ok": True}

    @allure.title("Создание дубликата курьера - ошибка 409")
    def test_create_duplicate_courier_error(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"],
            "firstName": courier["firstName"],
        }

        with allure.step("Повторно отправить POST /api/v1/courier"):
            response = requests.post(COURIER_URL, data=payload)

        with allure.step("Проверить код 409 и сообщение об ошибки"):
            assert response.status_code == STATUS_CONFLICT
            assert response.json()["message"] == COURIER_DUPLICATE_LOGIN_TEXT

    @allure.title("Создание курьера без поля '{mis_field}' - ошибка 400")
    @pytest.mark.parametrize("mis_field", ["login", "password"])
    def test_create_courier_mis_field(self, mis_field):
        payload = {
            "login": "test_login_" + mis_field,
            "password": "test_pass",
            "firstName": "test_name",
        }
        del payload[mis_field]

        with allure.step(f"Отправить POST /api/v1/courier без поля {mis_field}"):
            response = requests.post(COURIER_URL, data=payload)

        with allure.step("Проверить код 400 и текст ошибки"):
            assert response.status_code == STATUS_BAD_REQUEST
            assert response.json()["message"] == COURIER_CREATE_MIS_FIELD_TEXT