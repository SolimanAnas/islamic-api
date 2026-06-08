from pydantic import BaseModel


class Zikr(BaseModel):
    label: str = ""
    arabic: str
    english: str = ""
    transliteration: str = ""
    repeat: int = 1
    source: str = ""
    audio: str = ""


class ZikrChapter(BaseModel):
    id: str
    title_ar: str
    title_en: str = ""
    audio: str = ""
    items: list[Zikr]
