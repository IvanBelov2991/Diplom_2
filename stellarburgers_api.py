import allure
import requests
import urls


class StellarburgersApi:

    @staticmethod
    @allure.step('Отправка запроса на создание пользователя')
    def create_user(body):
        return requests.post(urls.BASE_URL + urls.CREATE_USER_ENDPOINT, json=body)

    @staticmethod
    @allure.step('Отправка запроса на авторизацию пользователя')
    def auth_user(body):
        return requests.post(urls.BASE_URL + urls.AUTH_USER_ENDPOINT, json=body)

    @staticmethod
    @allure.step('Отправка запроса на получение данных о пользователе')
    def get_user_data(user_token):
        headers = {
            'Authorization': user_token
        }
        get_user_data_request = requests.get(urls.BASE_URL + urls.USER_DATA_ENDPOINT, headers=headers)
        return get_user_data_request

    @staticmethod
    @allure.step('Отправка запроса на изменение данных о пользователе')
    def change_user_data(user_token, email, password, name):
        headers = {
            'Authorization': user_token
        }
        data = {
            'email': email,
            'password': password,
            'name': name
        }
        change_user_data_request = requests.patch(urls.BASE_URL + urls.USER_DATA_ENDPOINT, headers=headers, json=data)
        return change_user_data_request

    @staticmethod
    @allure.step('Отправка запроса на удаление пользователя')
    def delete_user(user_token):
        headers = {
            'Authorization': user_token
        }
        delete_request = requests.delete(urls.BASE_URL + urls.DELETE_USER_ENDPOINT, headers=headers)
        return delete_request

    @staticmethod
    @allure.step('Отправка запроса на создание заказа')
    def create_order(body):
        order_requests = requests.post(urls.BASE_URL + urls.CREATE_ORDER_ENDPOINT, json=body)
        return order_requests

    @staticmethod
    @allure.step('Отправка запроса на получение заказов пользователем')
    def get_order(user_token):
        headers = {
            'Authorization': user_token
        }
        order_requests = requests.get(urls.BASE_URL + urls.CREATE_ORDER_ENDPOINT, headers=headers)
        return order_requests

    @staticmethod
    @allure.step('Отправка запроса на получение заказа без токена')
    def get_order_without_auth():
        order_requests = requests.get(urls.BASE_URL + urls.CREATE_ORDER_ENDPOINT)
        return order_requests
