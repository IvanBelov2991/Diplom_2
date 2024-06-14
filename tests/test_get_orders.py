import allure
from stellarburgers_api import StellarburgersApi


class TestCreateOrder:
    @allure.title('Проверка запроса на получение заказов авторизованым пользователем')
    @allure.description("Проверка получения заказов авторизованным пользователем,"
                        " проверка кода и тела успешного ответа")
    def test_success_get_orders(self, default_user):
        auth_response, _, _, _, _ = default_user
        user_token = auth_response.json()["accessToken"]
        get_order_response = StellarburgersApi.get_order(user_token)

        assert get_order_response.status_code == 200
        assert get_order_response.json()["success"] == True
        assert get_order_response.json()["orders"] == []

    @allure.title('Проверка запроса на получение заказов без создания пользователя')
    @allure.description("Проверка получения заказов без создания пользователя, проверка кода,"
                        " ожидание неуспешного ответа")
    def test_cannot_get_orders_without_creation_user(self):
        get_order_response = StellarburgersApi.get_order_without_auth()

        assert get_order_response.status_code == 401
        assert get_order_response.json()["message"] == "You should be authorised"

    @allure.title('Проверка запроса на получение заказов неавторизованным пользователем')
    @allure.description("Проверка получения заказов без создания пользователя,"
                        " проверка кода, ожидание неуспешного ответа")
    def test_cannot_get_orders_without_auth(self, default_user_without_auth):
        user_response, email, password, name = default_user_without_auth
        user_token_creation = user_response.json()["accessToken"]
        get_order_response = StellarburgersApi.get_order(user_token_creation)

        assert get_order_response.status_code == 401
        # возвращает 200, это баг
        assert get_order_response.json()["message"] == "You should be authorised"
