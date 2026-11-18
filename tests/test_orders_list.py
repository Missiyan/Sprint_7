import allure
import requests
from scripts import BASE_URL


@allure.feature("Заказ")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов — успех")
    def test_get_orders_list(self):
        with allure.step("Отправить GET /api/v1/orders"):
            response = requests.get(f'{BASE_URL}/api/v1/orders')

        with allure.step("Проверить код 200 и что orders — список"):
            assert response.status_code == 200
            body = response.json()
            assert "orders" in body
            assert isinstance(body["orders"], list)