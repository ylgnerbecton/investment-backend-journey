# import pytest
# from fastapi import status
#
#
# class TestLocalWeatherView:
#     @pytest.fixture(autouse=True)
#     async def setup_and_teardown(self, mongo_db_session):
#         self.test_local_weather_name = "Lisboa"
#         self.collection = mongo_db_session["local_weather"]
#         yield
#         await self.collection.delete_many({"name": self.test_local_weather_name})
#
#     @pytest.mark.asyncio
#     async def test_post_local_weather(self, test_client):
#         response = await test_client.post(
#             "/local-weather", json={"name": self.test_local_weather_name}
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         response_body = response.json()
#
#         assert "response_data" in response_body
#         response_data = response_body["response_data"]
#         assert "name" in response_data
#         assert response_data["name"] == self.test_local_weather_name
#         assert "description" in response_data
#         assert "specs" in response_data
#         assert "created_at" in response_data
#         assert "updated_at" in response_data
#
#         inserted_document = await self.collection.find_one(
#             {"name": self.test_local_weather_name}
#         )
#         assert inserted_document is not None
#         assert inserted_document["name"] == self.test_local_weather_name
#
#     @pytest.mark.asyncio
#     async def test_post_local_weather_error_handling(self, test_client):
#         response = await test_client.post("/local-weather", json={"name": 123})
#         assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


import pytest
from fastapi import status


class TestUserView:

    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self, mysql_db_session):
        self.test_user_cpf = "12345678901"
        self.collection = mysql_db_session["users"]
        yield
        await self.collection.delete_many({"cpf": self.test_user_cpf})

    @pytest.mark.asyncio
    async def test_post_user(self, test_client):
        user_payload = {
            "name": "Test Name",
            "cpf": self.test_user_cpf,
            "email": "test@example.com",
            "password": "test_password",
            "birthdate": "2000-01-01",
            "phone": "1234567890"
        }
        response = await test_client.post("/user", json=user_payload)

        assert response.status_code == status.HTTP_201_CREATED
        response_body = response.json()

        assert "response_data" in response_body
        response_data = response_body["response_data"]
        assert "name" in response_data
        assert response_data["name"] == user_payload["name"]
        assert "email" in response_data

        inserted_user = await self.collection.find_one({"cpf": self.test_user_cpf})
        assert inserted_user is not None
        assert inserted_user["name"] == user_payload["name"]

    @pytest.mark.asyncio
    async def test_get_users(self, test_client):
        response = await test_client.get("/user")
        assert response.status_code == status.HTTP_200_OK
        response_body = response.json()

        assert "response_data" in response_body
        assert len(response_body["response_data"]) >= 1

    @pytest.mark.asyncio
    async def test_get_user_by_uuid(self, test_client):
        response = await test_client.get(f"/user/{self.test_user_cpf}")
        assert response.status_code == status.HTTP_200_OK
        response_body = response.json()

        assert "response_data" in response_body
        response_data = response_body["response_data"]
        assert "name" in response_data
        assert response_data["name"] == "Test Name"

    @pytest.mark.asyncio
    async def test_update_user(self, test_client):
        update_payload = {
            "name": "Updated Name"
        }
        response = await test_client.put(f"/user/{self.test_user_cpf}", json=update_payload)
        assert response.status_code == status.HTTP_200_OK
        response_body = response.json()

        assert "response_data" in response_body
        response_data = response_body["response_data"]
        assert "name" in response_data
        assert response_data["name"] == "Updated Name"

    @pytest.mark.asyncio
    async def test_delete_user(self, test_client):
        response = await test_client.delete(f"/user/{self.test_user_cpf}")
        assert response.status_code == status.HTTP_200_OK

        deleted_user = await self.collection.find_one({"cpf": self.test_user_cpf})
        assert deleted_user is None
