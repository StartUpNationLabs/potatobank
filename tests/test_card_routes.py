from fastapi.testclient import TestClient
from src.security import security_manager

def test_post_and_get_cart(client: TestClient):
    # Get server's public key
    response = client.get("/api/keys/")
    server_public_key = response.json()["public_key"]

    # Create test card
    test_pubkey = "test_public_key"
    encrypted_pubkey = security_manager.encrypt(test_pubkey, server_public_key)
    client.post(f"/api/cards/?pubkey_base64={encrypted_pubkey}")

    # Post cart
    test_cart = "test_cart_content"
    response = client.post(
        f"/api/cart/{encrypted_pubkey}",
        json=test_cart
    )
    assert response.status_code == 200

    # Get cart
    response = client.get(f"/api/cart/{encrypted_pubkey}")
    assert response.status_code == 200
    carts = response.json()
    assert len(carts) == 1
    assert carts[0] == test_cart

def test_get_cart_nonexistent_card(client: TestClient):
    # Get server's public key
    response = client.get("/api/keys/")
    server_public_key = response.json()["public_key"]

    # Try to get cart for non-existent card
    test_pubkey = "nonexistent_public_key"
    encrypted_pubkey = security_manager.encrypt(test_pubkey, server_public_key)
    response = client.get(f"/api/cart/{encrypted_pubkey}")
    assert response.status_code == 404
