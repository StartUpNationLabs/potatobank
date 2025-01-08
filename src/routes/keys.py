from fastapi import APIRouter

from src.security import security_manager

router = APIRouter()

@router.get("/keys/")
def read_keys():
    """
    Returns the public key of the API server.<br>
    <br>
    Returns: The base64 encoded public key.
    """
    try:
        return {
            "public_key": security_manager.get_public_key_base64()
        }
    except Exception:
        return {"error": "Failed to get public key"}
