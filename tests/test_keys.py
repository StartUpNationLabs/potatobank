def test_read_keys(client):
    response = client.get("/api/keys/")
    assert response.status_code == 200
    assert "public_key" in response.json()
