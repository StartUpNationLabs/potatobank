import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class SecurityManager:
    def __init__(self):
        self._private_key = None
        self._public_key = None
        self._generate_keys()

    def _generate_keys(self) -> None:
        """Generate RSA key pair (2048 bits)"""
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self._public_key = self._private_key.public_key()

    def get_public_key_base64(self) -> str:
        """Return the public key in base64 format"""
        pem = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return base64.b64encode(pem).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt data that was encrypted with the server's public key

        Args:
            encrypted_data: Base64 encoded encrypted data

        Returns:
            Decrypted data as string
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted_data = self._private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def encrypt(self, data: str, public_key_base64: str) -> str:
        """
        Encrypt data with a provided public key

        Args:
            data: String to encrypt
            public_key_base64: Base64 encoded public key to encrypt with

        Returns:
            Base64 encoded encrypted data
        """
        try:
            public_key_bytes = base64.b64decode(public_key_base64)
            public_key = serialization.load_pem_public_key(
                public_key_bytes,
                backend=default_backend()
            )
            encrypted_data = public_key.encrypt(
                data.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return base64.b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def sign(self, data: str) -> str:
        """
        Sign data with server's private key

        Args:
            data: String to sign

        Returns:
            Base64 encoded signature
        """
        signature = self._private_key.sign(
            data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')

    def verify_signature(self, data: str, signature: str, public_key_base64: str) -> bool:
        """
        Verify a signature using a public key

        Args:
            data: Original data that was signed
            signature: Base64 encoded signature
            public_key_base64: Base64 encoded public key to verify with

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            public_key_bytes = base64.b64decode(public_key_base64)
            public_key = serialization.load_pem_public_key(
                public_key_bytes,
                backend=default_backend()
            )
            signature_bytes = base64.b64decode(signature)

            public_key.verify(
                signature_bytes,
                data.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False

# Create a singleton instance
security_manager = SecurityManager()
