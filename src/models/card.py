from sqlmodel import SQLModel


class Card(SQLModel, table=True):
    pubkey: str
