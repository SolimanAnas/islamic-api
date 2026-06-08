from pydantic import BaseModel


class PrayerTimes(BaseModel):
    fajr: str
    sunrise: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str
    sunset: str = ""


class City(BaseModel):
    name: str
    lat: float
    lng: float
    country: str = ""
