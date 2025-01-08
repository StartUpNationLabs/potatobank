from fastapi import APIRouter

from src.database import SessionDep

router = APIRouter()


@router.post("/cards/")
def create_card(pubkey_base64: str, session: SessionDep):
    """
    Create a new card.<br>
    <br>
    :param pubkey_base64: The base64-encoded public key of the card encrypted with the bank's public key.<br>
    <br>
    :return: The newly created card.
    """
    pass
