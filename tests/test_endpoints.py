from httpx import AsyncClient, ASGITransport

from fastapi import status
import pytest

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


from app.database.sql_database import get_session
from app import models
from config import API_URL
from main import app


BASE_URL = "http://test"
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

transport = ASGITransport(app=app)


async def override_get_session():
    session = TestSessionLocal()
    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        yield session
    finally:
        await session.close()


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Q!16werty!23",
    }


@pytest.fixture
def auth_headers(event_loop, test_user_data):
    async def get_headers():
        login_payload = test_user_data
        async with AsyncClient(
            transport=transport,
            base_url=BASE_URL,
        ) as client:
            response = await client.post(
                f"{API_URL}/auth/token",
                json=login_payload,
            )
            assert response.status_code == 200, f"Login failed: {response.json()}"

            login_data = response.json()
            access_token = login_data["access_token"]

            return {
                "Authorization": f"Bearer {access_token}",
            }

    return event_loop.run_until_complete(get_headers())


@pytest.mark.asyncio
async def test_register_user_with_no_username(
    test_user_data,
):
    test_user_data.pop("username")
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{API_URL}/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_register_user_with_no_email(test_user_data):
    test_user_data.pop("email")
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{API_URL}/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_register_user_with_not_correct_pwd(test_user_data):
    test_user_data["password"] = "not_correct_pwd"
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{API_URL}/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_register_user(test_user_data):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{API_URL}/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["username"] == test_user_data["username"]


@pytest.mark.asyncio
async def test_register_same_user(test_user_data):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{API_URL}/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_login_user(test_user_data):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{API_URL}/auth/token", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_no_authorized(auth_headers):
    auth_headers["Authorization"] = "Bearer bad_token"
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get(
            f"{API_URL}/trades/get-last-trading-dates", headers=auth_headers
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_wrong_url(auth_headers):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get(f"{API_URL}/trades/wrong_url", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_last_trading_dates(auth_headers):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get(
            f"{API_URL}/trades/get-last-trading-dates", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5
        assert "size" in data


@pytest.mark.asyncio
async def test_get_dynamics(auth_headers):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get(
            f"{API_URL}/trades/get-dynamics", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5
        assert "items" in data


@pytest.mark.asyncio
async def test_get_trading_results(auth_headers):
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get(
            f"{API_URL}/trades/get-last-trading-dates", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5
        assert "total" in data
