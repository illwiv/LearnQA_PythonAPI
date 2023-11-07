from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_jast_created_user(self):
        # REG
        register_data = self.prepare_registration_data()
        responce1 = MyRequests.post(url='/user', data=register_data)

        Assertions.asser_code_status(responce1, expected_status_code=200)
        Assertions.assert_json_has_key(responce1, name="id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(responce1, name='id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        responce2 = MyRequests.post(url='/user/login', data=login_data)

        auth_sid = self.get_cookie(responce2, cookie_name='auth_sid')
        token = self.get_header(responce2, headers_name='x-csrf-token')

        # EDIT
        new_name = "Changed Name"

        responce3 = MyRequests.put(
            url=f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.asser_code_status(responce3, expected_status_code=200)

        # GET
        responce4 = MyRequests.get(
            url=f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            responce4,
            name="firstName",
            expected_value=new_name,
            error_message="Wrong name of the after edit"
        )
