import allure
import pytest
import helper
from stellarburgers_api import StellarburgersApi


@allure.step("Создание нового пользователя и удаление данных после завершения теста")
@pytest.fixture(scope='function')
def default_user():
    user_data = helper.UserFactory.user_with_random_data()
    user_response = StellarburgersApi.create_user(user_data)
    auth_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    auth_response = StellarburgersApi.auth_user(auth_data)
    yield user_response, auth_response, user_data['email'], user_data['password'], user_data['name']

    user_token = auth_response.json()["accessToken"]
    StellarburgersApi.delete_user(user_token)


@allure.step("Создание нового пользователя без авторизации")
@pytest.fixture(scope='function')
def default_user_without_auth():
    user_data = helper.UserFactory.user_with_random_data()
    user_response = StellarburgersApi.create_user(user_data)
    user_token_creation = user_response.json()["accessToken"]

    yield user_response, user_data['email'], user_data['password'], user_data['name']

    StellarburgersApi.delete_user(user_token_creation)
