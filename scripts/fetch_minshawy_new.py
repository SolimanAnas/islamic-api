"""Download the "المنشاوي المرتل الجديد" MediaFire folder as tagged MP3s.

Files are saved as <NN>.mp3 (NN = track number from the source filename),
non-MP3 sources are converted with ffmpeg, all source tags and cover art are
replaced with Zad Al-Muslim tags carrying the proper surah names and
Al-Minshawy-new/cover.jpg as album art, and index.json is written next to them with the GitHub Release download URLs.

Usage: python scripts/fetch_minshawy_new.py [OUTPUT_DIR]
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

FOLDER_KEY = "njszpoqikb8a4"
RELEASE_BASE = "https://github.com/SolimanAnas/islamic-api/releases/download/al-minshawy-new"
LIST_URL = (
    "https://www.mediafire.com/api/1.5/folder/get_content.php"
    f"?folder_key={FOLDER_KEY}&content_type=files&response_format=json&chunk_size=1000"
)

ARTIST = "Zad Al-Muslim App - تطبيق زاد المسلم"
ALBUM = "المصحف المرتل الجديد - الشيخ محمد صديق المنشاوي"
COVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Al-Minshawy-new", "cover.jpg")

# Surah segments per source track: (surah,) for a complete surah,
# (surah, from, to) for an ayah range, or a plain string for the full title.
# Tracks 30, 37 and 45 are not in the source folder.
TRACKS = {
    1: [("الفاتحة",), ("البقرة", 1, 61)],
    2: [("البقرة", 62, 112)],
    3: [("البقرة", 113, 171)],
    4: [("البقرة", 172, 217)],
    5: [("البقرة", 218, 255)],
    6: [("البقرة", 256, 286), ("آل عمران", 1, 18)],
    7: [("آل عمران", 19, 78)],
    8: [("آل عمران", 79, 148)],
    9: [("آل عمران", 149, 200), ("النساء", 1, 6)],
    10: [("النساء", 7, 63)],
    11: [("النساء", 64, 130)],
    12: [("النساء", 131, 176), ("المائدة", 1, 5)],
    13: [("المائدة", 6, 53)],
    14: [("المائدة", 54, 111)],
    15: [("المائدة", 112, 120), ("الأنعام", 1, 58)],
    16: [("الأنعام", 59, 127)],
    17: [("الأنعام", 128, 165), ("الأعراف", 1, 35)],
    18: [("الأعراف", 36, 103)],
    19: [("الأعراف", 104, 177)],
    20: [("الأعراف", 178, 206), ("الأنفال", 1, 44)],
    21: [("الأنفال", 45, 75), ("التوبة", 1, 35)],
    22: [("التوبة", 36, 103)],
    23: [("التوبة", 104, 129), ("يونس", 1, 36)],
    24: [("يونس", 37, 109), ("هود", 1, 8)],
    25: [("هود", 9, 83)],
    26: [("هود", 84, 123), ("يوسف", 1, 35)],
    27: [("يوسف", 36, 101)],
    28: [("يوسف", 102, 111), ("الرعد",), ("إبراهيم", 1, 11)],
    29: [("إبراهيم", 12, 52), ("الحجر",)],
    31: [("النحل", 98, 128), ("الإسراء", 1, 81)],
    32: [("الإسراء", 82, 111), ("الكهف", 1, 57)],
    33: [("الكهف", 58, 110), ("مريم", 1, 75)],
    34: [("مريم", 76, 98), ("طه", 1, 128)],
    35: [("طه", 129, 135), ("الأنبياء",)],
    36: [("الحج",)],
    38: [("النور", 21, 64), ("الفرقان", 1, 20)],
    39: [("الفرقان", 21, 77), ("الشعراء", 1, 140)],
    40: [("الشعراء", 141, 227), ("النمل", 1, 64)],
    41: [("النمل", 65, 93), ("القصص", 1, 70)],
    42: [("القصص", 71, 88), ("العنكبوت",), ("الروم", 1, 11)],
    43: [("الروم", 12, 60), ("لقمان",), ("السجدة", 1, 22)],
    44: [("السجدة", 23, 30), ("الأحزاب",)],
    46: [("فاطر", 37, 45), ("يس",), ("الصافات", 1, 74)],
    47: [("الصافات", 75, 182), ("ص",)],
    48: [("الزمر",), ("غافر", 1, 22)],
    49: [("غافر", 23, 85), ("فصلت", 1, 38)],
    50: [("فصلت", 39, 54), ("الشورى",), ("الزخرف", 1, 35)],
    51: [("الزخرف", 36, 89), ("الدخان",), ("الجاثية",), ("الأحقاف", 1, 14)],
    52: [("الأحقاف", 15, 35), ("محمد",), ("الفتح",)],
    53: [("الحجرات",), ("ق",), ("الذاريات",), ("الطور",), ("النجم", 1, 30)],
    54: [("النجم", 31, 62), ("القمر",), ("الرحمن",), ("الواقعة", 1, 74)],
    55: [("الواقعة", 75, 96), ("الحديد",), ("المجادلة",), ("الحشر", 1, 7)],
    56: [("الحشر", 8, 24), ("الممتحنة",), ("الصف",), ("الجمعة",), ("المنافقون",)],
    57: [("التغابن",), ("الطلاق",), ("التحريم",), ("الملك",), ("القلم", 1, 33)],
    58: [("القلم", 34, 52), ("الحاقة",), ("المعارج",), ("نوح",), ("الجن",), ("المزمل", 1, 19)],
    59: [("المزمل", 19, 20), ("المدثر",), ("القيامة",), ("الإنسان",), ("المرسلات",), ("النبأ",)],
    60: "من سورة النازعات إلى سورة الأعلى",
    61: "من سورة الغاشية إلى سورة الناس ودعاء ختم القرآن",
}


def track_title(segments):
    if isinstance(segments, str):
        return segments
    parts = [f"{s[0]} ({s[1]} - {s[2]})" if len(s) == 3 else s[0] for s in segments]
    return ("سورة " if len(parts) == 1 else "سور ") + "، ".join(parts)


def list_files():
    with urllib.request.urlopen(LIST_URL) as resp:
        return json.load(resp)["response"]["folder_content"]["files"]


def direct_link(page_url):
    page = subprocess.run(["curl", "-sSL", page_url], capture_output=True, text=True).stdout
    match = re.search(r'href="(https://download[^"]+)"', page)
    if not match:
        raise RuntimeError(f"no download link on {page_url}")
    return match.group(1)


def download(entry, dest):
    size = int(entry["size"])
    for _ in range(5):
        if os.path.exists(dest) and os.path.getsize(dest) == size:
            return
        subprocess.run(["curl", "-sSL", "--retry", "4", "-o", dest, direct_link(entry["links"]["normal_download"])])
    raise RuntimeError(f"failed to download {entry['filename']}")


def encode(src, dest, number, title):
    """Write dest from src's audio plus COVER, with fresh tags (MP3 is stream-copied)."""
    codec = ["-c:a", "copy"] if src.lower().endswith(".mp3") else ["-c:a", "libmp3lame", "-b:a", "192k", "-ar", "48000"]
    tags = {
        "title": title,
        "artist": ARTIST,
        "album_artist": ARTIST,
        "album": ALBUM,
        "publisher": ARTIST,
        "genre": "Quran",
        "track": str(number),
    }
    meta = [arg for k, v in tags.items() for arg in ("-metadata", f"{k}={v}")]
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", src, "-i", COVER, "-map", "0:a", "-map", "1:v", *codec,
         "-c:v", "copy", "-disposition:v", "attached_pic", "-metadata:s:v", "comment=Cover (front)",
         "-map_metadata", "-1", *meta, "-id3v2_version", "3", "-write_id3v1", "0", "-fflags", "+bitexact", "-f", "mp3", dest],
        check=True,
    )


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "Al-Minshawy-new"
    tmp_dir = os.path.join(out_dir, ".src")
    os.makedirs(tmp_dir, exist_ok=True)

    tracks = []
    for entry in sorted(list_files(), key=lambda e: e["filename"]):
        number, ext = entry["filename"].split("_", 1)[0], os.path.splitext(entry["filename"])[1]
        title = track_title(TRACKS[int(number)])
        mp3 = os.path.join(out_dir, f"{number}.mp3")

        src = os.path.join(tmp_dir, f"{number}{ext}")
        download(entry, src)
        encode(src, mp3, int(number), title)
        os.remove(src)
        print("OK", number, flush=True)

        tracks.append({
            "track": int(number),
            "file": f"{number}.mp3",
            "title": title,
            "size": os.path.getsize(mp3),
            "url": f"{RELEASE_BASE}/{number}.mp3",
        })

    os.rmdir(tmp_dir)
    index = {
        "reciter": "محمد صديق المنشاوي",
        "reciter_en": "Mohamed Siddiq Al-Minshawi",
        "collection": "المصحف المرتل الجديد",
        "riwayah": "حفص عن عاصم",
        "source": f"https://www.mediafire.com/folder/{FOLDER_KEY}",
        "tracks": tracks,
    }
    with open(os.path.join(out_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
