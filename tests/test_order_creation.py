import allure
import pytest
import requests
from scripts import BASE_URL, build_order_payload

@allure.feature("Заказ")
@allure.story("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_colors(self, color):
        payload = build_order_payload(color)
        with allure.step(f"Отправить POST /api/v1/orders с color={color}"):
            response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
        with allure.step("Проверить код 201 и наличие track"):
            assert response.status_code == 201
            assert "track" in response.json()