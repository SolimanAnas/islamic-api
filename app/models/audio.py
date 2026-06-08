from pydantic import BaseModel


class RadioStation(BaseModel):
    name: str
    url: str
    country: str = ""


class Reciter(BaseModel):
    id: str
    name: str
    type: str = "surah"
    base_url: str = ""
