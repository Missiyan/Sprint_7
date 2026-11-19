import allure
import requests
from urls import ORDERS_URL
from data import STATUS_OK


@allure.feature("Заказ")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов – успех")
    def test_get_orders_list(self):
        with allure.step("Отправить GET /api/v1/orders"):
            response = requests.get(ORDERS_URL)

        with allure.step("Проверить код 200 и что orders – список"):
            assert response.status_code == STATUS_OK
            body = response.json()
            assert "orders" in body
            assert isinstance(body["orders"], list)