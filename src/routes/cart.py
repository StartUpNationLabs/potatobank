from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.database import SessionDep, save
from src.models.card import Card
from src.models.cart import Cart
from src.security import security_manager

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
    try:
        # Decrypt the encrypted public key
        decrypted_pubkey = security_manager.decrypt(pubkey_base64)

        # Verify card exists
        card = session.exec(
            select(Card).where(Card.pubkey == decrypted_pubkey)
        ).first()

        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        # Get all carts for this card
        carts = session.exec(
            select(Cart).where(Cart.card_pubkey == decrypted_pubkey)
        ).all()

        return [cart.encrypted_content for cart in carts]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

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
    try:
        # Decrypt the encrypted public key
        decrypted_pubkey = security_manager.decrypt(pubkey_base64)

        # Verify card exists
        card = session.exec(
            select(Card).where(Card.pubkey == decrypted_pubkey)
        ).first()

        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        # Create new cart
        cart = Cart(
            card_pubkey=decrypted_pubkey,
            encrypted_content=cart_base64
        )
        save(session, cart)

        return True

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
