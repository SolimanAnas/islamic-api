<div align="center">

# ☪ Islamic API

### Free Islamic Data API — Quran, Hadith, Adhkar, Tafsir & More

A comprehensive REST API providing authenticated Islamic data for developers building Muslim-focused applications.

**[Live API](https://islamic-api.fly.dev)** · **[Interactive Docs](https://islamic-api.fly.dev/docs)** · **[GitHub](https://github.com/SolimanAnas/islamic-api)**

---

![Quran Ayahs](https://img.shields.io/badge/Quran-6%2C236%20Ayahs-059669?style=for-the-badge)
![Hadith](https://img.shields.io/badge/Hadith-13%20Collections-d4a843?style=for-the-badge)
![Adhkar](https://img.shields.io/badge/Adhkar-132%20Chapters-8b5cf6?style=for-the-badge)
![Tafsir](https://img.shields.io/badge/Tafsir-4%20Books-ec4899?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)

</div>

---

## Quick Start

```bash
# Get all 114 Quran surahs
curl https://islamic-api.fly.dev/v1/quran/surahs

# Search Hadith
curl "https://islamic-api.fly.dev/v1/hadith/search?q=prayer"

# Get Hisn Muslim chapters
curl https://islamic-api.fly.dev/v1/azkar/hisn/chapters

# Get tafsir for Ayat al-Kursi
curl https://islamic-api.fly.dev/v1/tafsir/ibn-kathir/2/255

# Get prayer times
curl "https://islamic-api.fly.dev/v1/prayer/times?city=Cairo"
```

> **No API key required.** Just make a request and get your data.

---

## API Endpoints

### 📖 Quran (`/v1/quran`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/quran/surahs` | List all 114 surahs |
| `GET /v1/quran/surah/{id}` | Get surah with all ayahs |
| `GET /v1/quran/ayah/{surah}/{ayah}` | Get a single ayah |
| `GET /v1/quran/juz/{id}` | Get all ayahs in a juz (1-30) |
| `GET /v1/quran/page/{number}` | Get ayahs on a mushaf page (1-604) |
| `GET /v1/quran/search?q={text}` | Search Quran text |

### 📚 Hadith (`/v1/hadith`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/hadith/collections` | List all 13 collections |
| `GET /v1/hadith/{collection}` | Get collection (paginated) |
| `GET /v1/hadith/{collection}/{id}` | Get a single hadith |
| `GET /v1/hadith/{collection}/sections` | List sections/chapters |
| `GET /v1/hadith/search?q={text}` | Search across collections |
| `GET /v1/hadith/random/{collection}` | Random hadith |

### 🏰 Adhkar (`/v1/azkar`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/azkar/hisn/chapters` | List all Hisn Muslim chapters |
| `GET /v1/azkar/hisn/{id}` | Get chapter with all items |
| `GET /v1/azkar/morning` | Morning adhkar |
| `GET /v1/azkar/evening` | Evening adhkar |
| `GET /v1/azkar/sleeping` | Sleeping adhkar |
| `GET /v1/azkar/post-salah` | Post-salah adhkar |
| `GET /v1/azkar/search?q={text}` | Search all adhkar |

### 📝 Tafsir (`/v1/tafsir`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/tafsir/books` | List available tafsir books |
| `GET /v1/tafsir/{book}/{surah}` | Tafsir for a surah |
| `GET /v1/tafsir/{book}/{surah}/{ayah}` | Tafsir for a specific ayah |
| `GET /v1/tafsir/{book}/search?q={text}` | Search within tafsir |

### 🕌 Prayer (`/v1/prayer`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/prayer/times?city={city}` | Prayer times for a city |
| `GET /v1/prayer/times?lat={lat}&lon={lon}` | Prayer times by coordinates |
| `GET /v1/prayer/cities` | List 287+ cities |

### 📻 Audio (`/v1/audio`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/audio/stations` | 150+ Quran radio stations |
| `GET /v1/audio/reciters` | 40+ Quran reciters |

### 🤲 Duas (`/v1/duas`)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/duas/books` | List all dua books |
| `GET /v1/duas/{bookId}` | Get a dua book |
| `GET /v1/duas/search?q={text}` | Search across duas |

---

## Response Format

All endpoints return consistent JSON:

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

---

## Data Sources

| Dataset | Source | Count |
|---------|--------|-------|
| **Quran Text** | Uthmani script (verified) | 6,236 ayahs |
| **Sahih al-Bukhari** | sunnah.com | ~7,563 hadith |
| **Sahih Muslim** | sunnah.com | ~5,363 hadith |
| **Sunan Abu Dawud** | sunnah.com | ~4,590 hadith |
| **Jami at-Tirmidhi** | sunnah.com | ~3,956 hadith |
| **Sunan an-Nasa'i** | sunnah.com | ~5,095 hadith |
| **Sunan Ibn Majah** | sunnah.com | ~4,341 hadith |
| **Mishkat al-Masabih** | Verified | ~4,428 hadith |
| **Riyad as-Salihin** | Imam Nawawi | ~1,896 hadith |
| **Bulugh al-Maram** | Ibn Hajar | ~1,767 hadith |
| **Al-Adab Al-Mufrad** | Imam al-Bukhari | ~1,326 hadith |
| **Shama'il Muhammadiyah** | Imam al-Tirmidhi | ~402 hadith |
| **40 Hadith Qudsi** | Compiled | 40 hadith |
| **40 Hadith Nawawi** | Imam al-Nawawi | 42 hadith |
| **Hisn Muslim** | Dr. al-Qahtani | 132 chapters |
| **Tafsir** | Ibn Kathir, Qurtubi, Baghawi, Sa'di | 4 books |

---

## Run Locally

```bash
git clone https://github.com/SolimanAnas/islamic-api.git
cd islamic-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for interactive API documentation.

### Docker

```bash
docker-compose up --build
```

---

## Deployment

### Fly.io (Recommended — Free)

```bash
fly auth login
fly launch
fly deploy
```

### Railway ($5/month)

```bash
railway login
railway init
railway up
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full deployment guide.

---

## Project Structure

```
islamic-api/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings
│   ├── models/              # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── services/            # Data loader
│   └── utils/               # Pagination helpers
├── data/                    # Islamic data files
│   ├── quran/               # Quran text (Uthmani)
│   ├── hadith/              # 13 hadith collections
│   ├── azkar/               # Hisn Muslim + adhkar
│   ├── tafsir/              # 4 tafsir SQLite DBs
│   ├── duas/                # 5 dua books
│   ├── prayer/              # 287+ cities
│   └── audio/               # Radio & reciters
├── tests/                   # 55 pytest tests
├── docs/                    # Documentation
├── index.html               # Landing page
├── Dockerfile
├── fly.toml
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

<div align="center">

**Built with ❤ for the Ummah**

*Data sourced from [sunnah.com](https://sunnah.com), [quran.com](https://quran.com), and [hisnmuslim.com](https://hisnmuslim.com)*

</div>
