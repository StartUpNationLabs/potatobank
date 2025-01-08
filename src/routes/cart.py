from typing import List

from fastapi import APIRouter

from src.database import SessionDep

router = APIRouter()


@router.get("/cart/{pubkey_base64}")
async def get_cart(pubkey_base64: str, session: SessionDep) -> List[str]:
    """
    Get the cart of a user<br>
    <br>
    pubkey_base64: str: The base64 encoded public key of the user encrypted with the server's public key<br>
    <br>
    Returns: List[str]: The list of base64 encoded carts encrypted with the user's public key
    """
    return []


@router.post("/cart/{pubkey_base64}")
async def post_cart(pubkey_base64: str, cart_base64: str, session: SessionDep) -> bool:
    """
    Add a cart to a user<br>
    <br>
    pubkey_base64: str: The base64 encoded public key of the user encrypted with the server's public key<br>
    cart_base64: str: The base64 encoded cart encrypted with the user's public key<br>
    <br>
    Returns: bool: True if the cart was added successfully (validated by the server's private key)
    """
    return True
