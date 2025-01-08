import pytest

from src.security import SecurityManager


@pytest.fixture
def security():
    return SecurityManager()

def test_key_generation(security):
    assert security._private_key is not None
    assert security._public_key is not None

def test_get_public_key_base64(security):
    public_key = security.get_public_key_base64()
    assert isinstance(public_key, str)
    assert len(public_key) > 0

def test_encryption_decryption(security):
    # Test data
    original_data = "test message"

    # Get public key and encrypt
    public_key = security.get_public_key_base64()
    encrypted = security.encrypt(original_data, public_key)

    # Decrypt and verify
    decrypted = security.decrypt(encrypted)
    assert decrypted == original_data

def test_signing_verification(security):
    # Test data
    data = "test message"

    # Sign data
    signature = security.sign(data)

    # Verify signature
    public_key = security.get_public_key_base64()
    assert security.verify_signature(data, signature, public_key)

def test_invalid_signature_verification(security):
    # Test data
    data = "test message"
    wrong_data = "wrong message"

    # Sign data
    signature = security.sign(data)

    # Verify with wrong data
    public_key = security.get_public_key_base64()
    assert not security.verify_signature(wrong_data, signature, public_key)
