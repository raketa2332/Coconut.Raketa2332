from constants.constant import BASE_URL
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"

    def __init__(self, session):
        super().__init__(session=session, base_url=self.USER_BASE_URL)

    def get_user_info(self, user_locator, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_locator}",
            expected_status=expected_status)

    def create_user(self, user_data: dict, expected_status: int = 201):
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    def update_user(self, user_id: str, data: dict, expected_status: int = 200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=data,
            expected_status=expected_status
        )