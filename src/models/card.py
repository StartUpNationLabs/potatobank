from typing import Optional

from sqlmodel import Field, SQLModel


class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pubkey: str = Field(index=True, unique=True)


class CardDTO(SQLModel):
    pubkey: str
