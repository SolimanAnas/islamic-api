"""Download the "المنشاوي المرتل الجديد" MediaFire folder as MP3s.

Files are saved as <NN>.mp3 (NN = track number from the source filename),
non-MP3 sources are converted with ffmpeg, and index.json is written next to
them with the original titles and the GitHub Release download URLs.

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


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "Al-Minshawy-new"
    tmp_dir = os.path.join(out_dir, ".src")
    os.makedirs(tmp_dir, exist_ok=True)

    tracks = []
    for entry in sorted(list_files(), key=lambda e: e["filename"]):
        name = entry["filename"]
        number, title = name.split("_", 1)
        title, ext = os.path.splitext(title)
        mp3 = os.path.join(out_dir, f"{number}.mp3")

        if not os.path.exists(mp3):
            src = os.path.join(tmp_dir, f"{number}{ext}")
            download(entry, src)
            if ext.lower() == ".mp3":
                os.replace(src, mp3)
            else:
                subprocess.run(
                    ["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-c:a", "libmp3lame",
                     "-b:a", "192k", "-ar", "48000", mp3],
                    check=True,
                )
                os.remove(src)
        print("OK", number, flush=True)

        tracks.append({
            "track": int(number),
            "file": f"{number}.mp3",
            "title": title.replace("_", " "),
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
