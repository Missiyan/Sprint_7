import allure
import pytest
import uuid
import requests
from scripts import BASE_URL, login_courier, delete_courier

@allure.feature("Курьер")
@allure.story("Создание курьера")
class TestCourierCreation:

    @allure.title("Создание курьера - успех")
    def test_create_courier_success(self):
        login = "courier_" + uuid.uuid4().hex[:10]
        payload = {"login": login, "password": "pass", "firstName": "name"}

        with allure.step("Отправить POST /api/v1/courier"):
            response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

        with allure.step("Проверить код 201 и тело {'ok': true}"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

        # очистка
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

        with allure.step("Повторно отправить POST /api/v1/courier с тем же логином"):
            response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

        with allure.step("Проверить код 409"):
            assert response.status_code == 409

    @allure.title("Создание курьера без поля '{mis_field}' — ошибка 400")
    @pytest.mark.parametrize("mis_field", ["login", "password"])
    def test_create_courier_mis_field(self, mis_field):
        payload = {
            "login": "test_login_" + mis_field,
            "password": "test_pass",
            "firstName": "test_name",
        }
        del payload[mis_field]

        with allure.step(f"Отправить POST /api/v1/courier без поля {mis_field}"):
            response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

        with allure.step("Проверить код 400 и текст ошибки"):
            assert response.status_code == 400
            assert "Недостаточно данных" in response.text