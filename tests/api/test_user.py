import pytest
from resources.user_creds import SuperAdminCreds


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data.model_dump(by_alias=True, exclude_unset=True)).json()

        assert response.get("id") and response["id"] != "", "id должен быть не пустым"
        assert response.get("email") == creation_user_data.email
        assert response.get("fullName") == creation_user_data.full_name
        assert response.get("roles", []) == creation_user_data.roles
        assert response.get("verified") is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(
            creation_user_data.model_dump(by_alias=True, exclude_unset=True)).json()
        response_by_id = super_admin.api.user_api.get_user_info(created_user_response["id"]).json()
        response_by_email = super_admin.api.user_api.get_user_info(created_user_response["email"]).json()

        assert response_by_id == response_by_email, "Содержимое ответов должно быть идентичным"
        assert response_by_id.get("id") and response_by_email["id"] != "", "id должен быть не пустым"
        assert response_by_id.get("email") == creation_user_data.email
        assert response_by_id.get("fullName") == creation_user_data.full_name
        assert response_by_id.get("roles", []) == creation_user_data.roles
        assert response_by_id.get("verified") is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)
