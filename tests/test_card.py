import base64


def test_create_card(client):
    # Encrypt a public key with the server's public key
    public_key = "test_public_key"
    response = client.get("/api/keys/")
    server_public_key = response.json()["public_key"]
    encrypted_pubkey = base64.b64encode(public_key.encode()).decode()

    response = client.post("/api/cards/", json={"pubkey_base64": encrypted_pubkey})
    assert response.status_code == 200
    assert "pubkey" in response.json()
    assert "signature" in response.json()

def test_create_existing_card(client):
    public_key = "test_public_key"
    encrypted_pubkey = base64.b64encode(public_key.encode()).decode()

    # Create the card for the first time
    client.post("/api/cards/", json={"pubkey_base64": encrypted_pubkey})

    # Try to create the same card again
    response = client.post("/api/cards/", json={"pubkey_base64": encrypted_pubkey})
    assert response.status_code == 400
    assert response.json()["detail"] == "Card already exists"
