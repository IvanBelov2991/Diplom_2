import allure
import pytest
import helper
from stellarburgers_api import StellarburgersApi


class TestCreateUser:
    @allure.title('Проверка успешного создания пользователя')
    @allure.description("Создание нового курьера, проверка статуса ответа и тела ответа")
    def test_success_create_user(self, default_user):
        user_response, _, _, _, _ = default_user
        assert user_response.status_code == 200 and user_response.json()["success"] == True, "Ожидался ответ True"

    @allure.title('Создание пользователя с уже существующим email')
    @allure.description("Повторное создание пользователя с тем же email возвращает ошибку")
    def test_cannot_create_user_with_existing_login(self, default_user):
        _, _, user_email, _, _ = default_user
        second_user_response = StellarburgersApi.create_user({"email": user_email, "password": "some_password",
                                                              "name": "some_name"})
        assert second_user_response.status_code == 403 \
               and second_user_response.json()["message"] == "User already exists"

    @allure.title('Создание пользователя c пустым логином')
    @allure.description("Создание пользователя c пустым email возвращает ошибку")
    def test_cannot_create_user_with_empty_email(self):
        new_user_data = helper.UserFactory.user_with_random_data()
        new_user_data["email"] = ""
        response = StellarburgersApi.create_user(new_user_data)
        assert response.status_code == 403 \
               and response.json()["message"] == "Email, password and name are required fields"

    @allure.title('Создание пользователя c пустым паролем')
    @allure.description("Создание пользователя c пустым паролем возвращает ошибку")
    # Пробел в поле должен считаться пустым паролем и выдавать ошибку 403
    @pytest.mark.parametrize("password", [
        pytest.param(' '),
        pytest.param('')
    ])
    def test_cannot_create_user_with_empty_password(self, password):
        new_user_data = helper.UserFactory.user_with_random_data()
        new_user_data["password"] = password
        response = StellarburgersApi.create_user(new_user_data)
        assert response.status_code == 403 \
               and response.json()["message"] == "Email, password and name are required fields"

    @allure.title('Создание пользователя c пустым именем')
    @allure.description("Создание пользователя c пустым именем возвращает ошибку")
    # Пробел в поле должен считаться пустым паролем и выдавать ошибку 403
    @pytest.mark.parametrize("name", [
        pytest.param(' '),
        pytest.param('')
    ])
    def test_cannot_create_user_with_empty_name(self, name):
        new_user_data = helper.UserFactory.user_with_random_data()
        new_user_data["name"] = name
        response = StellarburgersApi.create_user(new_user_data)
        assert response.status_code == 403 \
               and response.json()["message"] == "Email, password and name are required fields"
