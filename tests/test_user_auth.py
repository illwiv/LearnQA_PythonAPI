import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Auth cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post(url="/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, cookie_name="auth_sid")
        self.token = self.get_header(response1, headers_name="x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, name="user_id")
    @allure.description("This test successfully auth user by email and password")
    def test_user_auth(self):

        response2 = MyRequests.get(
            url="/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            name="user_id",
            expected_value=self.user_id_from_auth_method,
            error_message="User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test checks auth status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = MyRequests.get(
                url='/user/auth',
                headers={"x-csrf-token": self.token}
            )
        else:
            response2 = MyRequests.get(
                url='/user/auth',
                cookies={"auth_sid": self.auth_sid}
            )
        Assertions.assert_json_value_by_name(
            response2,
            name="user_id",
            expected_value=0,
            error_message="User id from auth method is not equal to user id from check method"
        )
