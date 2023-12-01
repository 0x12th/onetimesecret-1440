# tests/test_router.py

from httpx import AsyncClient


async def test_generate_secret_route(client: AsyncClient) -> None:
    response = await client.post(
        "/generate",
        json={
            "secret_message": "test_message",
            "passphrase": "test_passphrase",
            "ttl": 3600,
        },
    )
    assert response.status_code == 201
    assert "secret_key" in response.json()


async def test_get_secret_route(client: AsyncClient) -> None:
    generate_response = await client.post(
        "/generate",
        json={
            "secret_message": "test_message2",
            "passphrase": "test_passphrase2",
            "ttl": 3600,
        },
    )
    assert generate_response.status_code == 201
    generate_response_json = generate_response.json()
    secret_key = generate_response_json["secret_key"]

    response = await client.post(
        f"/secrets/{secret_key}", json={"passphrase": "test_passphrase2"}
    )

    assert response.status_code == 200
    assert "secret_message" in response.json()

    response = await client.post(
        f"/secrets/{secret_key}", json={"passphrase": "test_passphrase2"}
    )
    assert response.status_code == 404
