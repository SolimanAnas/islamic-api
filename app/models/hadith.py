from pydantic import BaseModel


class HadithSection(BaseModel):
    id: int
    name_ar: str
    name_en: str
    hadith_start: int
    hadith_end: int


class HadithCollection(BaseModel):
    id: str
    name_ar: str
    name_en: str
    total_hadith: int
    sections: list[HadithSection]


class Hadith(BaseModel):
    id: int
    collection: str
    book_number: int | None = None
    chapter_number: int | None = None
    section: str | None = None
    narrator: str | None = None
    arabic_text: str
    english_text: str | None = None
    grades: list[dict] = []
