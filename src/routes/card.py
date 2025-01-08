from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.database import SessionDep, save
from src.models.card import Card, CardDTO
from src.security import security_manager

router = APIRouter()


@router.post("/cards/")
def create_card(card_dto: CardDTO, session: SessionDep):
    """
    Create a new card.<br>
    <br>
    :param pubkey_base64: The base64-encoded public key of the card encrypted with the bank's public key.<br>
    <br>
    :return: The newly created card.
    """
    try:
        # Decrypt the encrypted public key
        decrypted_pubkey = security_manager.decrypt(card_dto.pubkey_base64)

        # Check if card already exists
        existing_card = session.exec(
            select(Card).where(Card.pubkey == decrypted_pubkey)
        ).first()

        if existing_card:
            raise HTTPException(status_code=400, detail="Card already exists")

        # Create new card
        new_card = Card(pubkey=decrypted_pubkey)
        save(session, new_card)

        return {
            "pubkey": decrypted_pubkey,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
