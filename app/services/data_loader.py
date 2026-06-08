import json
from pathlib import Path
from typing import Any

from app.config import DATA_DIR


class DataStore:
    """Central data store holding all loaded Islamic data in memory."""

    def __init__(self):
        self.quran_ayahs: list[dict] = []
        self.quran_surahs: list[dict] = []
        self.hadith_collections: dict[str, dict] = {}
        self.hisn_chapters: list[dict] = []
        self.azkar_morning: list[dict] = []
        self.azkar_evening: list[dict] = []
        self.azkar_sleeping: list[dict] = []
        self.salah: list[dict] = []
        self.dua_books: dict[str, dict] = {}
        self.radio_stations: list[dict] = []
        self.reciters: list[dict] = []
        self.cities: dict[str, dict] = {}
        self.hadith_index: dict = {}


_store: DataStore | None = None


def get_store() -> DataStore:
    global _store
    if _store is None:
        _store = DataStore()
    return _store


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_data():
    store = get_store()
    print("🔄 Loading Islamic data...")

    _load_quran(store)
    _load_hadith(store)
    _load_azkar(store)
    _load_duas(store)
    _load_audio(store)
    _load_prayer(store)

    total = (
        len(store.quran_surahs)
        + len(store.hadith_collections)
        + len(store.hisn_chapters)
        + len(store.azkar_morning)
        + len(store.azkar_evening)
        + len(store.azkar_sleeping)
        + len(store.radio_stations)
        + len(store.reciters)
    )
    print(f"✅ Loaded {total} data entries")


def _load_quran(store: DataStore):
    quran_path = DATA_DIR / "quran" / "quran.json"
    data = _load_json(quran_path)
    if not data:
        print("⚠️  quran.json not found")
        return

    store.quran_ayahs = data

    surah_map: dict[int, dict] = {}
    for ayah in data:
        s = ayah["surah"]
        if s not in surah_map:
            surah_map[s] = {
                "number": s,
                "name_ar": ayah.get("surah_name", ""),
                "name_en": ayah.get("surah_name_en", ""),
                "ayah_count": 0,
                "ayahs": [],
            }
        surah_map[s]["ayah_count"] += 1
        surah_map[s]["ayahs"].append(ayah)

    store.quran_surahs = [surah_map[k] for k in sorted(surah_map.keys())]
    print(f"  📖 Quran: {len(store.quran_surahs)} surahs, {len(store.quran_ayahs)} ayahs")


def _load_hadith(store: DataStore):
    hadith_dir = DATA_DIR / "hadith"
    collections = {
        "bukhari": ("Sahih al-Bukhari", "صحيح البخاري"),
        "muslim": ("Sahih Muslim", "صحيح مسلم"),
        "abudawud": ("Sunan Abu Dawud", "سنن أبي داود"),
        "tirmidhi": ("Jami at-Tirmidhi", "جامع الترمذي"),
        "nasai": ("Sunan an-Nasa'i", "سنن النسائي"),
        "ibnmajah": ("Sunan Ibn Majah", "سنن ابن ماجه"),
        "mishkat": ("Mishkat al-Masabih", "مشكاة المصابيح"),
        "riyad_assalihin": ("Riyad as-Salihin", "رياض الصالحين"),
        "bulugh_almaram": ("Bulugh al-Maram", "بُلُوغ المرام"),
        "aladab_almufrad": ("Al-Adab Al-Mufrad", "الأدب المفرد"),
        "shamail_muhammadiyah": ("Shama'il Muhammadiyah", "الشمائل المحمدية"),
        "qudsi40": ("40 Hadith Qudsi", "أربعون حديثاً قدسياً"),
        "nawawi40": ("40 Hadith Nawawi", "الأربعون النووية"),
    }

    for key, (name_en, name_ar) in collections.items():
        path = hadith_dir / f"{key}.json"
        data = _load_json(path)
        if not data:
            continue

        hadiths = data.get("hadiths", [])
        metadata = data.get("metadata", {})
        raw_sections = metadata.get("sections", {})

        sections = []
        for sec_id, sec_name in raw_sections.items():
            sections.append({
                "id": int(sec_id),
                "name_ar": sec_name if isinstance(sec_name, str) else "",
                "name_en": sec_name if isinstance(sec_name, str) else "",
                "hadith_start": 0,
                "hadith_end": 0,
            })

        store.hadith_collections[key] = {
            "id": key,
            "name_ar": name_ar,
            "name_en": name_en,
            "total_hadith": len(hadiths),
            "sections": sections,
            "hadiths": hadiths,
        }

    print(f"  📚 Hadith: {len(store.hadith_collections)} collections")


def _load_azkar(store: DataStore):
    azkar_path = DATA_DIR / "azkar" / "azkar.json"
    data = _load_json(azkar_path)
    if data:
        store.azkar_morning = data.get("morning", [])
        store.azkar_evening = data.get("evening", [])
        print(f"  🕌 Azkar: morning={len(store.azkar_morning)}, evening={len(store.azkar_evening)}")

    sleeping_path = DATA_DIR / "azkar" / "sleeping.json"
    data = _load_json(sleeping_path)
    if data:
        store.azkar_sleeping = data
        print(f"  🌙 Azkar: sleeping={len(store.azkar_sleeping)}")

    hisn_path = DATA_DIR / "azkar" / "hisn.json"
    data = _load_json(hisn_path)
    if data:
        store.hisn_chapters = data
        print(f"  🏰 Hisn Muslim: {len(store.hisn_chapters)} chapters")

    salah_path = DATA_DIR / "azkar" / "salah.json"
    data = _load_json(salah_path)
    if data:
        store.salah = data
        print(f"  🤲 Salah adhkar: {len(store.salah)}")


def _load_duas(store: DataStore):
    duas_dir = DATA_DIR / "duas"
    for i in range(1, 6):
        path = duas_dir / f"duaa-{i:02d}.json"
        data = _load_json(path)
        if data:
            store.dua_books[f"book-{i}"] = {
                "id": f"book-{i}",
                "title": data[0].get("title", f"Book {i}") if data else f"Book {i}",
                "items": data,
            }
    print(f"  📖 Duas: {len(store.dua_books)} books")


def _load_audio(store: DataStore):
    stations_path = DATA_DIR / "audio" / "stations.json"
    data = _load_json(stations_path)
    if data:
        store.radio_stations = data.get("stations", [])
        print(f"  📻 Radio: {len(store.radio_stations)} stations")

    reciters_path = DATA_DIR / "audio" / "reciters.json"
    data = _load_json(reciters_path)
    if data:
        store.reciters = data.get("reciters", [])
        print(f"  🎙️ Reciters: {len(store.reciters)}")


def _load_prayer(store: DataStore):
    cities_path = DATA_DIR / "prayer" / "cities.json"
    data = _load_json(cities_path)
    if data:
        store.cities = data
        print(f"  🕌 Cities: {len(store.cities)}")
