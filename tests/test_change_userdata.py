import allure
import helper
from stellarburgers_api import StellarburgersApi
from faker import Faker


class TestChangeUserData:
    @allure.title('Проверка запроса на изменение email авторизованного пользователя')
    @allure.description("Проверка запроса на изменение email пользователя, проверка кода и тела успешного ответа")
    def test_success_change_email(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        user_token = auth_response.json()["accessToken"]
        new_email = Faker().email()
        change_user_data_response = StellarburgersApi.change_user_data(
            user_token, email=new_email, password=user_password, name=user_name)
        assert change_user_data_response.status_code == 200
        assert change_user_data_response.json()["user"]["email"] == new_email
        assert change_user_data_response.json()["user"]["name"] == user_name
        assert change_user_data_response.json()["success"] == True

    @allure.title('Проверка запроса на изменение имени авторизованного пользователя')
    @allure.description("Проверка запроса на изменение имени пользователя, проверка кода и тела успешного ответа")
    def test_success_change_name(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        user_token = auth_response.json()["accessToken"]
        new_name = Faker().name()
        change_user_data_response = StellarburgersApi.change_user_data(
            user_token, email=user_email, password=user_password, name=new_name)
        assert change_user_data_response.status_code == 200
        assert change_user_data_response.json()["user"]["email"] == user_email
        assert change_user_data_response.json()["user"]["name"] == new_name
        assert change_user_data_response.json()["success"] == True

    @allure.title('Проверка запроса на изменение пароля авторизованного пользователя')
    @allure.description("Проверка запроса на изменение пароля пользователя, проверка кода и тела успешного ответа")
    def test_success_change_password(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        user_token = auth_response.json()["accessToken"]
        new_password = Faker().password()
        change_user_data_response = StellarburgersApi.change_user_data(
            user_token, email=user_email, password=new_password, name=user_name)
        assert change_user_data_response.status_code == 200
        assert change_user_data_response.json()["user"]["email"] == user_email
        assert change_user_data_response.json()["user"]["name"] == user_name
        assert change_user_data_response.json()["success"] == True

    @allure.title('Проверка запроса на изменение email на уже существующий email')
    @allure.description(
        "Проверка запроса на изменение email пользователя на уже существующий email, проверка получения ошибки")
    def test_cannot_change_email_to_existing_email(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user

        user_data_2, user_2_token = helper.Helper.create_user_with_auth_token(
            "existingemail@example.com", "password", "John Doe")  # создаю второго пользователя

        user_2_email = user_data_2["email"]

        user_token = auth_response.json()["accessToken"]
        change_user_data_response = StellarburgersApi.change_user_data(
            user_token, email=user_2_email, password=user_password, name=user_name)
        assert change_user_data_response.status_code == 403
        assert change_user_data_response.json()["success"] == False
        assert change_user_data_response.json()["message"] == "User with such email already exists"

        # Удаление второго пользователя (первый удаляется фикстурой)
        delete_user_2_data_response = StellarburgersApi.delete_user(user_2_token)
        assert delete_user_2_data_response.status_code == 202

    @allure.title('Проверка запроса на изменение email пользователя с невалидным токеном')
    @allure.description(
        "Проверка запроса на изменение email пользователя"
        " посредством ввода невалидного токена, проверка кода и тела ответа")
    def test_cannot_change_email_with_invalid_token(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        fake_token = "Bearer " + Faker().uuid4()
        new_email = Faker().email()
        change_user_data_response = StellarburgersApi.change_user_data(
            fake_token, email=new_email, password=user_password, name=user_name)
        assert change_user_data_response.status_code == 403
        assert change_user_data_response.json()['message'] == 'jwt malformed'
        assert change_user_data_response.json()['success'] == False

    @allure.title('Проверка запроса на изменение имени пользователя с невалидным токеном')
    @allure.description(
        "Проверка запроса на изменение имени пользователя"
        " посредством ввода невалидного токена, проверка кода и тела ответа")
    def test_cannot_change_name_with_invalid_token(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        fake_token = "Bearer " + Faker().uuid4()
        new_name = Faker().name()
        change_user_data_response = StellarburgersApi.change_user_data(
            fake_token, email=user_email, password=user_password, name=new_name)
        assert change_user_data_response.status_code == 403
        assert change_user_data_response.json()['message'] == 'jwt malformed'
        assert change_user_data_response.json()['success'] == False

    @allure.title('Проверка запроса на изменение пароля пользователя с невалидным токеном')
    @allure.description(
        "Проверка запроса на изменение пароля пользователя"
        " посредством ввода невалидного токена, проверка кода и тела ответа")
    def test_cannot_change_password_with_invalid_token(self, default_user):
        _, auth_response, user_email, user_password, user_name = default_user
        fake_token = "Bearer " + Faker().uuid4()
        new_password = Faker().password()
        change_user_data_response = StellarburgersApi.change_user_data(
            fake_token, email=user_email, password=new_password, name=user_name)
        assert change_user_data_response.status_code == 403
        assert change_user_data_response.json()['message'] == 'jwt malformed'
        assert change_user_data_response.json()['success'] == False
