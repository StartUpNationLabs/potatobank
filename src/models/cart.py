from typing import Optional

from sqlmodel import Field, SQLModel


class Cart(SQLModel, table=True):
    card_pubkey: Optional[int] = Field(default=None, foreign_key="card.pubkey")
