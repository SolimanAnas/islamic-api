from pydantic import BaseModel


class SurahSummary(BaseModel):
    number: int
    name_ar: str
    name_en: str
    ayah_count: int


class Ayah(BaseModel):
    surah: int
    ayah: int
    text_uthmani: str
    text_clean: str
    surah_name: str
    surah_name_en: str


class Surah(BaseModel):
    number: int
    name_ar: str
    name_en: str
    ayah_count: int
    ayahs: list[Ayah]
