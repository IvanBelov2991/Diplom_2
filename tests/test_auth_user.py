import allure
from faker import Faker
from helper import UserFactory
from stellarburgers_api import StellarburgersApi


class TestAuthUser:
    @allure.title('Проверка успешной авторизации пользователя')
    @allure.description("Авторизация существующего пользователя, проверка статуса ответа и тела ответа")
    def test_success_auth_user(self, default_user):
        _, auth_response, user_email, _, user_name = default_user
        assert auth_response.status_code == 200
        assert "accessToken" in auth_response.json()
        assert "refreshToken" in auth_response.json()
        assert auth_response.json()["user"]["email"] == user_email
        assert auth_response.json()["user"]["name"] == user_name

    @allure.title('Неуспешная авторизация при запросе без пароля')
    @allure.description("Авторизация не проходит, если не введен пароль")
    def test_cannot_auth_user_with_empty_password(self, default_user):
        _, _, user_email, _, _ = default_user
        auth_courier_response_with_empty_password = StellarburgersApi.auth_user({
            "email": user_email, "password": ""})

        assert auth_courier_response_with_empty_password.status_code == 401
        assert auth_courier_response_with_empty_password.json()["success"] == False
        assert auth_courier_response_with_empty_password.json()["message"] == "email or password are incorrect"

    @allure.title('Неуспешная авторизация при запросе с неверным паролем')
    @allure.description("Авторизация не проходит, введен неверный пароль")
    def test_cannot_auth_user_with_invalid_password(self, default_user):
        _, _, user_email, _, _ = default_user
        auth_courier_response_with_invalid_password = StellarburgersApi.auth_user({
            "email": user_email, "password": "random_password"})

        assert auth_courier_response_with_invalid_password.status_code == 401
        assert auth_courier_response_with_invalid_password.json()["success"] == False
        assert auth_courier_response_with_invalid_password.json()["message"] == "email or password are incorrect"

    @allure.title('Неуспешная авторизация при запросе без email')
    @allure.description("Авторизация не проходит, если не введен email")
    def test_cannot_auth_user_with_empty_email(self, default_user):
        _, _, _, user_password, _ = default_user
        auth_courier_response_with_empty_email = StellarburgersApi.auth_user({
            "email": "", "password": user_password})

        assert auth_courier_response_with_empty_email.status_code == 401
        assert auth_courier_response_with_empty_email.json()["success"] == False
        assert auth_courier_response_with_empty_email.json()["message"] == "email or password are incorrect"

    @allure.title('Неуспешная авторизация при запросе c невалидным email')
    @allure.description("Авторизация не проходит, если введен невалидный email")
    def test_cannot_auth_user_with_invalid_email(self, default_user):
        _, _, _, user_password, _ = default_user
        auth_courier_response_with_invalid_email = StellarburgersApi.auth_user({
            "email": "random_email", "password": user_password})

        assert auth_courier_response_with_invalid_email.status_code == 401
        assert auth_courier_response_with_invalid_email.json()["success"] == False
        assert auth_courier_response_with_invalid_email.json()["message"] == "email or password are incorrect"

    @allure.title('Неуспешная авторизация при вводе невалидных данных')
    @allure.description("Проверка: нельзя авторизоваться, если ввести несуществующие данные")
    def test_cannot_auth_user_with_invalid_email_and_pass(self):
        response = StellarburgersApi.auth_user(UserFactory.user_with_random_data())
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "email or password are incorrect"


class TestGetUserData:
    @allure.title('Проверка запроса на получение данных авторизованного пользователя')
    @allure.description(
        "Проверка запроса на получение данных авторизованного пользователя, проверка кода и тела успешного ответа")
    def test_success_get_userdata(self, default_user):
        _, auth_response, user_email, _, user_name = default_user
        user_token = auth_response.json()["accessToken"]
        get_user_data_response = StellarburgersApi.get_user_data(user_token)
        assert get_user_data_response.status_code == 200
        assert get_user_data_response.json()["user"]["email"] == user_email
        assert get_user_data_response.json()["user"]["name"] == user_name
        assert get_user_data_response.json()["success"] == True

    @allure.title('Проверка запроса на получение данных авторизованного пользователя с невалидным токеном')
    @allure.description(
        "Проверка запроса на получение данных авторизованного пользователя"
        " посредством ввода невалидного токена, проверка кода и тела ответа")
    def test_can_not_get_userdata_with_invalid_token(self, default_user):
        _, _, _, _, _ = default_user
        fake_token = "Bearer " + Faker().uuid4()
        get_user_data_response = StellarburgersApi.get_user_data(fake_token)
        assert get_user_data_response.status_code == 403
        assert get_user_data_response.json()['message'] == 'jwt malformed'
        assert get_user_data_response.json()['success'] == False
