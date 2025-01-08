from fastapi import APIRouter

router = APIRouter()


@router.get("/keys/")
def read_keys():
    """
    Returns the public key of the API server.<br>
    <br>
    Returns: The base64 encoded public key.
    """
    pass
