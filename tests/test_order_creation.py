import allure
import pytest
import requests
from urls import ORDERS_URL
from data import ORDER_COLORS, STATUS_CREATED
from scripts import build_order_payload

@allure.feature("Заказ")
@allure.story("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_create_order_with_colors(self, color):
        payload = build_order_payload(color)

        with allure.step(f"Отправить POST /api/v1/orders с color={color}"):
            response = requests.post(ORDERS_URL, json=payload)

        with allure.step("Проверить код 201 и наличие track"):
            assert response.status_code == STATUS_CREATED
            assert "track" in response.json()