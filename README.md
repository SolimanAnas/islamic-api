# Islamic API

**Free Islamic Data API — Quran, Hadith, Adhkar, Tafsir & More**

A comprehensive REST API providing authenticated Islamic data for developers building Muslim-focused applications. All data is sourced from verified Islamic references.

> **Base URL:** `https://islamic-api.vercel.app`
> **Docs:** `https://islamic-api.vercel.app/docs` (Swagger UI)
> **Redoc:** `https://islamic-api.vercel.app/redoc`

---

## Quick Start

### Use the API (no setup needed)

```bash
# Get all 114 Quran surahs
curl https://islamic-api.vercel.app/v1/quran/surahs

# Get Surah Al-Fatiha
curl https://islamic-api.vercel.app/v1/quran/surah/1

# Search Quran
curl "https://islamic-api.vercel.app/v1/quran/search?q=الرحمن&lang=ar"

# Get Hadith from Bukhari
curl "https://islamic-api.vercel.app/v1/hadith/bukhari?page=1&per_page=5"

# Get Hisn Muslim chapters
curl https://islamic-api.vercel.app/v1/azkar/hisn/chapters

# Get morning adhkar
curl https://islamic-api.vercel.app/v1/azkar/morning

# Get prayer times
curl "https://islamic-api.vercel.app/v1/prayer/times?city=Cairo"

# Get radio stations
curl https://islamic-api.vercel.app/v1/audio/stations
```

### Run locally

```bash
git clone https://github.com/SolimanAnas/islamic-api.git
cd islamic-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for interactive API documentation.

### Run with Docker

```bash
docker-compose up --build
```

---

## API Endpoints

### Quran (`/v1/quran`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/quran/surahs` | List all 114 surahs |
| `GET` | `/v1/quran/surah/{id}` | Get surah with all ayahs |
| `GET` | `/v1/quran/ayah/{surah}/{ayah}` | Get a single ayah |
| `GET` | `/v1/quran/juz/{id}` | Get all ayahs in a juz (1-30) |
| `GET` | `/v1/quran/page/{number}` | Get ayahs on a mushaf page (1-604) |
| `GET` | `/v1/quran/search?q={text}` | Search Quran text |

### Hadith (`/v1/hadith`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/hadith/collections` | List all 13 collections |
| `GET` | `/v1/hadith/{collection}` | Get collection (paginated) |
| `GET` | `/v1/hadith/{collection}/{id}` | Get a single hadith |
| `GET` | `/v1/hadith/{collection}/sections` | List sections/chapters |
| `GET` | `/v1/hadith/search?q={text}` | Search across collections |
| `GET` | `/v1/hadith/random/{collection}` | Random hadith |

### Adhkar (`/v1/azkar`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/azkar/hisn/chapters` | List all Hisn Muslim chapters |
| `GET` | `/v1/azkar/hisn/{id}` | Get chapter with all items |
| `GET` | `/v1/azkar/morning` | Morning adhkar |
| `GET` | `/v1/azkar/evening` | Evening adhkar |
| `GET` | `/v1/azkar/sleeping` | Sleeping adhkar |
| `GET` | `/v1/azkar/post-salah` | Post-salah adhkar |
| `GET` | `/v1/azkar/search?q={text}` | Search all adhkar |

### Tafsir (`/v1/tafsir`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/tafsir/books` | List available tafsir books |
| `GET` | `/v1/tafsir/{book}/{surah}` | Tafsir for a surah |
| `GET` | `/v1/tafsir/{book}/{surah}/{ayah}` | Tafsir for a specific ayah |
| `GET` | `/v1/tafsir/{book}/search?q={text}` | Search within tafsir |

### Prayer Times (`/v1/prayer`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/prayer/times?city={city}` | Prayer times for a city |
| `GET` | `/v1/prayer/times?lat={lat}&lon={lon}` | Prayer times by coordinates |
| `GET` | `/v1/prayer/cities` | List 200+ cities |

### Audio (`/v1/audio`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/audio/stations` | 150+ Quran radio stations |
| `GET` | `/v1/audio/reciters` | 40+ Quran reciters |

### Duas (`/v1/duas`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/duas/books` | List all dua books |
| `GET` | `/v1/duas/{bookId}` | Get a dua book |
| `GET` | `/v1/duas/search?q={text}` | Search across duas |

---

## Data Sources

All data is sourced from authenticated Islamic references:

| Dataset | Source | Count |
|---------|--------|-------|
| **Quran Text** | Uthmani script (verified) | 6,236 ayahs, 114 surahs |
| **Sahih al-Bukhari** | sunnah.com verified | ~7,563 hadith |
| **Sahih Muslim** | sunnah.com verified | ~5,363 hadith |
| **Sunan Abu Dawud** | sunnah.com verified | ~4,590 hadith |
| **Jami at-Tirmidhi** | sunnah.com verified | ~3,956 hadith |
| **Sunan an-Nasa'i** | sunnah.com verified | ~5,095 hadith |
| **Sunan Ibn Majah** | sunnah.com verified | ~4,341 hadith |
| **Mishkat al-Masabih** | Verified compilation | ~4,428 hadith |
| **Riyad as-Salihin** | Imam Nawawi | ~1,896 hadith |
| **Bulugh al-Maram** | Ibn Hajar al-Asqalani | ~1,767 hadith |
| **Al-Adab Al-Mufrad** | Imam al-Bukhari | ~1,326 hadith |
| **Shama'il Muhammadiyah** | Imam al-Tirmidhi | ~402 hadith |
| **40 Hadith Qudsi** | Compiled collection | 40 hadith |
| **40 Hadith Nawawi** | Imam al-Nawawi | 42 hadith |
| **Hisn Muslim** | Dr. Said bin Wahf al-Qahtani | 132 chapters |
| **Morning/Evening Adhkar** | Verified prophetic adhkar | ~50 adhkar |
| **Tafsir al-Qurtubi** | SQLite database | Complete |
| **Tafsir Ibn Kathir** | SQLite database | Complete |
| **Tafsir al-Baghawi** | SQLite database | Complete |
| **Tafsir as-Sa'di** | SQLite database | Complete |

---

## Response Format

All endpoints return a consistent JSON structure:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 6236,
    "total_pages": 312
  }
}
```

Paginated endpoints include `meta` with pagination info. Non-paginated endpoints return just `success` and `data`.

---

## Authentication

No authentication required. This is a free, open API.

If you deploy your own instance and want rate limiting, add API key support via the `X-API-Key` header.

---

## Deployment

### Vercel (Recommended — Free)

1. Fork this repo
2. Connect to Vercel
3. Vercel auto-detects `app/main.py`
4. Deploy

### Railway ($5/month)

```bash
railway login
railway init
railway up
```

### Fly.io (Free tier)

```bash
fly auth login
fly launch
fly deploy
```

### Self-hosted

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Project Structure

```
islamic-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment settings
│   ├── models/              # Pydantic response schemas
│   │   ├── common.py        # APIResponse, PaginatedResponse
│   │   ├── quran.py         # Surah, Ayah models
│   │   ├── hadith.py        # Hadith, Collection models
│   │   ├── azkar.py         # Zikr, ZikrChapter models
│   │   ├── tafsir.py        # TafsirEntry model
│   │   ├── prayer.py        # PrayerTimes, City models
│   │   ├── audio.py         # RadioStation, Reciter models
│   │   └── duas.py          # DuaBook, DuaItem models
│   ├── routers/             # API endpoint handlers
│   │   ├── quran.py
│   │   ├── hadith.py
│   │   ├── azkar.py
│   │   ├── tafsir.py
│   │   ├── prayer.py
│   │   ├── audio.py
│   │   └── duas.py
│   ├── services/            # Business logic
│   │   ├── data_loader.py   # Load JSON/SQLite at startup
│   │   └── cache.py
│   └── utils/
│       └── pagination.py    # Pagination & search helpers
├── data/                    # Islamic data files
│   ├── quran/               # Quran text (Uthmani script)
│   ├── hadith/              # 13 hadith collections
│   ├── azkar/               # Hisn Muslim + morning/evening/sleeping
│   ├── duas/                # 5 books of comprehensive duas
│   ├── prayer/              # City coordinates
│   └── audio/               # Radio stations & reciters
├── docs/
│   ├── ENDPOINTS.md         # Full API reference
│   ├── DATA.md              # Data sources & attribution
│   └── DEPLOYMENT.md        # Deployment guide
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── LICENSE
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Data sourced from [sunnah.com](https://sunnah.com), [quran.com](https://quran.com), and [hisnMuslim.com](https://hisnmuslim.com)
- Tafsir databases compiled from authenticated sources
- Built with [FastAPI](https://fastapi.tiangolo.com/)
