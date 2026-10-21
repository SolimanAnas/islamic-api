# Al-Minshawy — المصحف المرتل الجديد

Murattal recitation by Sheikh Mohamed Siddiq Al-Minshawi (Hafs 'an 'Asim), 58 MP3 tracks (~2.4 GB).

The audio is not stored in git. It is published as assets of the
[`al-minshawy-new` release](https://github.com/SolimanAnas/islamic-api/releases/tag/al-minshawy-new):

```
https://github.com/SolimanAnas/islamic-api/releases/download/al-minshawy-new/<NN>.mp3
```

[`index.json`](index.json) lists every track with its Arabic title (surah/ayah range), size and URL.
Track numbers follow the source folder; 30, 37 and 45 are missing from the source.

To download the files locally (requires `curl` and `ffmpeg`):

```
python scripts/fetch_minshawy_new.py Al-Minshawy-new
```

The [release workflow](../.github/workflows/minshawy-release.yml) runs the same script and uploads the result.
