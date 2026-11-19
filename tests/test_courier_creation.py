import allure
import pytest
import uuid
import requests
from urls import COURIER_URL
from data import (
    COURIER_CREATE_MIS_FIELD_TEXT,
    STATUS_CREATED,
    STATUS_BAD_REQUEST,
    STATUS_CONFLICT,
)
from scripts import login_courier, delete_courier

@allure.feature("Курьер")
@allure.story("Создание курьера")
class TestCourierCreation:

    @allure.title("Создание курьера - успех")
    def test_create_courier_success(self):
        login = "courier_" + uuid.uuid4().hex[:10]
        payload = {"login": login, "password": "pass", "firstName": "name"}

        try:
            with allure.step("Отправить POST /api/v1/courier"):
                response = requests.post(COURIER_URL, data=payload)

            with allure.step("Проверить код 201 и тело {'ok': true}"):
                assert response.status_code == STATUS_CREATED
                assert response.json() == {"ok": True}
        finally:
            with allure.step("Удалить курьера после теста"):
                courier_id = login_courier(login, "pass")
                if courier_id:
                    delete_courier(courier_id)

    @allure.title("Создание дубликата курьера - ошибка 409")
    def test_create_duplicate_courier_error(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"],
            "firstName": courier["firstName"],
        }

        with allure.step("Повторно отправить POST /api/v1/courier"):
            response = requests.post(COURIER_URL, data=payload)

        with allure.step("Проверить код 409 и сообщение об ошибке"):
            assert response.status_code == STATUS_CONFLICT
            assert "message" in response.json()

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
            assert COURIER_CREATE_MIS_FIELD_TEXT in response.text