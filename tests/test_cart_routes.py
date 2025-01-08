from fastapi.testclient import TestClient

from src.security import security_manager


def test_create_card(client: TestClient):
    # Get server's public key
    response = client.get("/api/keys/")
    assert response.status_code == 200
    server_public_key = response.json()["public_key"]

    # Create test card public key
    test_pubkey = "test_public_key"
    encrypted_pubkey = security_manager.encrypt(test_pubkey, server_public_key)

    # Create card
    response = client.post(f"/api/cards/?pubkey_base64={encrypted_pubkey}")
    assert response.status_code == 200

    # Verify response
    data = response.json()
    assert data["pubkey"] == test_pubkey
    assert "signature" in data

def test_create_duplicate_card(client: TestClient):
    # Get server's public key
    response = client.get("/api/keys/")
    server_public_key = response.json()["public_key"]

    # Create test card public key
    test_pubkey = "test_public_key"
    encrypted_pubkey = security_manager.encrypt(test_pubkey, server_public_key)

    # Create first card
    client.post(f"/api/cards/?pubkey_base64={encrypted_pubkey}")

    # Try to create duplicate card
    response = client.post(f"/api/cards/?pubkey_base64={encrypted_pubkey}")
    assert response.status_code == 400
