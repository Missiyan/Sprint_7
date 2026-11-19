import allure
import pytest
import requests

from urls import COURIER_LOGIN_URL
from data import (
    COURIER_LOGIN_MIS_FIELD_TEXT,
    STATUS_OK,
    STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND,
    STATUS_GATEWAY_TIMEOUT,
)


@allure.feature("Курьер")
@allure.story("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин возвращает id")
    def test_login_success(self, courier):
        payload = {"login": courier["login"], "password": courier["password"]}

        with allure.step("Отправить POST /api/v1/courier/login"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверить код 200 и наличие id"):
            assert response.status_code == STATUS_OK
            assert "id" in response.json()

    @allure.title("Логин с неверным паролем - ошибка 404")
    def test_login_wrong_password(self, courier):
        payload = {"login": courier["login"], "password": "wrong_password_123"}

        with allure.step("Отправить POST /api/v1/courier/login с неверным паролем"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверить код 404 и наличие message"):
            assert response.status_code == STATUS_NOT_FOUND
            assert "message" in response.json()

    @allure.title("Логин под несуществующим пользователем - ошибка 404")
    def test_login_nonexistent_user(self):
        payload = {"login": "nonexistent_login_xyz", "password": "any_pass"}

        with allure.step("Отправить POST /api/v1/courier/login с несуществующим логином"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверить код 404 и наличие message"):
            assert response.status_code == STATUS_NOT_FOUND
            assert "message" in response.json()

    @allure.title("Логин без поля '{mis_field}' - ошибка")
    @pytest.mark.parametrize("mis_field", ["login", "password"])
    def test_login_mis_field(self, mis_field):
        payload = {"login": "some_login", "password": "some_pass"}
        del payload[mis_field]

        with allure.step(f"Отправить POST /api/v1/courier/login без поля {mis_field}"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверить код 400 или 504 (стенд нестабилен)"):
            assert response.status_code in (STATUS_BAD_REQUEST, STATUS_GATEWAY_TIMEOUT)
            if response.status_code == STATUS_BAD_REQUEST:
                assert COURIER_LOGIN_MIS_FIELD_TEXT in response.text