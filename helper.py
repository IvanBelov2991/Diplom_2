import random
import allure
from faker import Faker

from stellarburgers_api import StellarburgersApi


class UserFactory:
    @staticmethod
    @allure.step("Генерация body для создания пользователя")
    def user_with_random_data():
        fake = Faker()
        email = fake.email()
        password = fake.password()
        name = fake.name()

        return {
            "email": email,
            "password": password,
            "name": name
        }

class Helper:
    @staticmethod
    def create_user_with_auth_token(email, password, name):
        user_data = {
            "email": email,
            "password": password,
            "name": name
        }
        StellarburgersApi.create_user(user_data)
        auth_response = StellarburgersApi.auth_user({"email": email, "password": password})
        user_token = auth_response.json()["accessToken"]
        return user_data, user_token

