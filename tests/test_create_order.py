import allure
from stellarburgers_api import StellarburgersApi
import data


class TestCreateOrder:
    @allure.title('Проверка запроса на создание заказа авторизованым пользователем')
    @allure.description("Проверка создание запроса авторизованным пользователем, проверка кода и тела успешного ответа")
    def test_success_create_order(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        create_order_response = StellarburgersApi.create_order(data.order_body)

        assert create_order_response.status_code == 200
        assert create_order_response.json()["success"] == True

    @allure.title('Проверка запроса на создание заказа неавторизованым пользователем')
    @allure.description("Проверка создание запроса неавторизованным пользователем, проверка кода и тела ответа")
    def test_cannot_create_order_by_unauthorized_user(self):
        create_order_response = StellarburgersApi.create_order(data.order_body)

        assert create_order_response.status_code == 400  # статус 200 - баг

    @allure.title('Проверка запроса на создание заказа - выбран только соус')
    @allure.description("Проверка запроса на создание заказа только с соусом, проверка кода и тела ответа")
    def test_cannot_create_order_with_only_sause_ingredient(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        create_order_response = StellarburgersApi.create_order(data.sauce_ingredient)

        assert create_order_response.status_code == 400

    @allure.title('Проверка запроса на создание заказа - выбрана только начинка')
    @allure.description("Проверка запроса на создание заказа с начинкой, проверка кода и тела ответа")
    def test_cannot_create_order_with_only_filling_ingredient(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        create_order_response = StellarburgersApi.create_order(data.filling_ingredient)

        assert create_order_response.status_code == 400

    @allure.title('Проверка запроса на создание заказа без ингредиентов')
    @allure.description("Проверка создания заказа без указания ингредиентов, ожидание ошибочного ответа")
    def test_create_order_without_ingredients(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        empty_order_body = {"ingredients": []}
        create_order_response = StellarburgersApi.create_order(empty_order_body)

        assert create_order_response.status_code == 400
        assert create_order_response.json()["success"] == False
        assert create_order_response.json()["message"] == "Ingredient ids must be provided"

    @allure.title('Проверка запроса на создание заказа с неправильным хешем ингредиента')
    @allure.description("Проверка создания заказа с неправильным хешем ингредиента, ожидание ошибки 500")
    def test_create_order_with_incorrect_ingredient(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        create_order_response = StellarburgersApi.create_order(data.fake_ingredient)

        assert create_order_response.status_code == 500
        # баг, по документации должна возвращаться ошибка 500 (сейчас возвразается 400)
        assert create_order_response.json()["success"] == False
        assert create_order_response.json()["message"] == "One or more ids provided are incorrect"
