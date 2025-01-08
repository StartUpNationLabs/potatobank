from typing import Optional

from sqlmodel import Field, SQLModel


class CartDTO(SQLModel):
    cart_base64: str


class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_pubkey: str = Field(foreign_key="card.pubkey")
    encrypted_content: str  # Base64 encoded encrypted cart content
