"""Quran images service — URL builders and coordinate data for mushaf pages."""

from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "quran"

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/SolimanAnas/quran-data-library/main"

MUSHAF_VERSIONS = {
    "madina-1421": {
        "name": "Madina 1421",
        "format": "webp",
        "dir": "mushaf-pages/madina-1421",
        "description": "King Fahd Complex, Lafz Al-Jalalah highlighted",
    },
    "madina-green": {
        "name": "Madina Green",
        "format": "webp",
        "dir": "mushaf-pages/madina-green",
        "description": "Green-tinted background variant",
    },
    "mushaf-1024": {
        "name": "Standard 1024",
        "format": "png",
        "dir": "mushaf-pages/mushaf-1024",
        "description": "Standard Madina pages at 1024px width",
    },
    "mushaf-madina-1420": {
        "name": "Madina 1420",
        "format": "webp",
        "dir": "mushaf-pages/mushaf-madina-1420",
        "description": "Modern 1420 AH printing style",
    },
    "tajweed-colored": {
        "name": "Tajweed Colored",
        "format": "webp",
        "dir": "mushaf-pages/tajweed-colored",
        "description": "Color-coded Tajweed rules",
    },
    "madina-2-brown-border": {
        "name": "Brown Border",
        "format": "png",
        "dir": "mushaf-pages/Madina-2-Brown-Border",
        "description": "Brown border frame variant",
    },
}

FONT_DIR = "mushaf-fonts/qbc-v2"
LINE_DIR = "line-by-line"

_page_coordinates: dict = {}
_line_coordinates: dict = {}


def load_coordinates():
    """Load coordinate data at startup."""
    global _page_coordinates, _line_coordinates

    page_file = DATA_DIR / "coordinates" / "page-coordinates.json"
    if page_file.exists():
        import json
        with open(page_file, "r", encoding="utf-8") as f:
            _page_coordinates = json.load(f).get("pages", {})

    line_file = DATA_DIR / "coordinates" / "line-coordinates.json"
    if line_file.exists():
        import json
        with open(line_file, "r", encoding="utf-8") as f:
            _line_coordinates = json.load(f).get("pages", {})


def page_url(version: str, page: int) -> str:
    v = MUSHAF_VERSIONS.get(version)
    if not v:
        raise ValueError(f"Unknown version: {version}. Valid: {', '.join(MUSHAF_VERSIONS)}")
    return f"{GITHUB_RAW_BASE}/{v['dir']}/{page:03d}.{v['format']}"


def line_url(page: int, line: int) -> str:
    return f"{GITHUB_RAW_BASE}/{LINE_DIR}/{page}/{line}.png"


def font_url(page: int) -> str:
    return f"{GITHUB_RAW_BASE}/{FONT_DIR}/p{page}.woff2"


def get_page_coordinates(page: int) -> Optional[dict]:
    key = f"{page:03d}"
    return _page_coordinates.get(key)


def get_line_coordinates(page: int) -> Optional[dict]:
    key = f"{page:03d}"
    return _line_coordinates.get(key)


def get_line_forayah(page: int, surah: int, ayah: int) -> Optional[dict]:
    page_data = _line_coordinates.get(f"{page:03d}", {})
    lines = page_data.get("lines", {})
    for line_num, line_data in lines.items():
        if line_data.get("surah") == surah:
            if line_data.get("ayah_start") <= ayah <= line_data.get("ayah_end", ayah):
                return {"line": int(line_num), **line_data}
    return None
