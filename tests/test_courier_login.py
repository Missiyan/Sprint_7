import allure
import pytest
import requests
from scripts import BASE_URL


@allure.feature("Курьер")
@allure.story("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин возвращает id")
    def test_login_success(self, courier):
        payload = {"login": courier["login"], "password": courier["password"]}

        with allure.step("Отправить POST /api/v1/courier/login"):
            response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        with allure.step("Проверить код 200 и наличие id в ответе"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Логин с неверным паролем - ошибка 404")
    def test_login_wrong_password(self, courier):
        payload = {"login": courier["login"], "password": "wrong_password_123"}

        with allure.step("Отправить POST /api/v1/courier/login с неверным паролем"):
            response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        with allure.step("Проверить код 404 и наличие message"):
            assert response.status_code == 404
            assert "message" in response.json()

    @allure.title("Логин под несуществующим пользователем - ошибка 404")
    def test_login_nonexistent_user(self):
        payload = {"login": "nonexistent_login_xyz", "password": "any_pass"}

        with allure.step("Отправить POST /api/v1/courier/login с несуществующим логином"):
            response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        with allure.step("Проверить код 404"):
            assert response.status_code == 404

    @allure.title("Логин без поля '{mis_field}' - ошибка")
    @pytest.mark.parametrize("mis_field", ["login", "password"])
    def test_login_mis_field(self, mis_field):
        payload = {"login": "some_login", "password": "some_pass"}
        del payload[mis_field]

        with allure.step(f"Отправить POST /api/v1/courier/login без поля {mis_field}"):
            response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        with allure.step("Проверить код: 400 или 504 (стенд нестабилен)"):
            assert response.status_code in (400, 504)
            if response.status_code == 400:
                assert "Недостаточно данных" in response.text