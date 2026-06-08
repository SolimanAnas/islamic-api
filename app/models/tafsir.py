from pydantic import BaseModel


class TafsirEntry(BaseModel):
    surah: int
    ayah: int
    text: str
    source: str = ""
