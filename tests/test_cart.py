import base64


def test_post_cart(client):
    public_key = "test_public_key"
    encrypted_pubkey = base64.b64encode(public_key.encode()).decode()

    # Create the card first
    client.post("/api/cards/", json={"pubkey_base64": encrypted_pubkey})

    # Add a cart
    cart_content = "test_cart_content"
    encrypted_cart = base64.b64encode(cart_content.encode()).decode()
    response = client.post(f"/api/cart/{encrypted_pubkey}", json={"cart_base64": encrypted_cart})
    assert response.status_code == 200
    assert response.json() is True

def test_get_cart(client):
    public_key = "test_public_key"
    encrypted_pubkey = base64.b64encode(public_key.encode()).decode()

    # Create the card first
    client.post("/api/cards/", json={"pubkey_base64": encrypted_pubkey})

    # Add a cart
    cart_content = "test_cart_content"
    encrypted_cart = base64.b64encode(cart_content.encode()).decode()
    client.post(f"/api/cart/{encrypted_pubkey}", json={"cart_base64": encrypted_cart})

    # Get the cart
    response = client.get(f"/api/cart/{encrypted_pubkey}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == encrypted_cart

def test_get_cart_not_found(client):
    public_key = "non_existent_public_key"
    encrypted_pubkey = base64.b64encode(public_key.encode()).decode()

    response = client.get(f"/api/cart/{encrypted_pubkey}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"
