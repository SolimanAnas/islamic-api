from pydantic import BaseModel


class DuaItem(BaseModel):
    label: str = ""
    arabic: str
    reference: str = ""


class DuaBook(BaseModel):
    id: str
    title: str
    items: list[DuaItem]
