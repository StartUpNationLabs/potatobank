from fastapi.testclient import TestClient

from src.models.card import CardDTO
from src.security import security_manager


def test_post_card(client: TestClient):
    # Get server's public key
    response = client.get("/api/keys/")
    server_public_key = response.json()["public_key"]

    # Create test card
    test_pubkey = "test_public_key"
    encrypted_pubkey = security_manager.encrypt(test_pubkey, server_public_key)
    card_dto = CardDTO(pubkey_base64=encrypted_pubkey)
    response = client.post("/api/cards/", json=card_dto.dict())

    assert response.status_code == 200
    assert response.json()["pubkey"] == test_pubkey
