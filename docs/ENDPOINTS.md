# API Endpoints Reference

## Base URL

```
https://islamic-api.vercel.app
```

All endpoints return JSON. Pagination is available on list endpoints via `page` and `per_page` query parameters (default: `page=1`, `per_page=20`).

---

## Quran

### List all surahs

```
GET /v1/quran/surahs
```

Returns all 114 surahs with number, Arabic name, English name, and ayah count.

### Get a surah

```
GET /v1/quran/surah/{id}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | Surah number (1-114) |

Returns the surah with all its ayahs in Uthmani script.

### Get an ayah

```
GET /v1/quran/ayah/{surah}/{ayah}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `surah` | int | Surah number (1-114) |
| `ayah` | int | Ayah number within the surah |

### Get a juz

```
GET /v1/quran/juz/{id}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | Juz number (1-30) |

### Get a mushaf page

```
GET /v1/quran/page/{number}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `number` | int | Page number (1-604) |

### Search Quran

```
GET /v1/quran/search?q={text}&lang={lang}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query (min 2 chars) |
| `lang` | string | `ar` | Language: `ar` or `en` |
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page (1-100) |

---

## Hadith

### List collections

```
GET /v1/hadith/collections
```

Returns all 13 available hadith collections.

**Collections:** bukhari, muslim, abudawud, tirmidhi, nasai, ibnmajah, mishkat, riyad_assalihin, bulugh_almaram, aladab_almufrad, shamail_muhammadiyah, qudsi40, nawawi40

### Get a collection

```
GET /v1/hadith/{collection}?page={page}&per_page={per_page}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `collection` | string | required | Collection ID |
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page (1-100) |

### Get a hadith

```
GET /v1/hadith/{collection}/{id}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `collection` | string | Collection ID |
| `id` | int | Hadith number |

### Get sections

```
GET /v1/hadith/{collection}/sections
```

### Search hadith

```
GET /v1/hadith/search?q={text}&collection={collection}&lang={lang}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query (min 2 chars) |
| `collection` | string | null | Limit to specific collection |
| `lang` | string | `en` | Language: `ar` or `en` |
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page (1-100) |

### Random hadith

```
GET /v1/hadith/random/{collection}
```

---

## Adhkar

### Hisn Muslim chapters

```
GET /v1/azkar/hisn/chapters
```

Returns all 132 chapters of Hisn Muslim.

### Get a chapter

```
GET /v1/azkar/hisn/{id}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Chapter ID (e.g., "ch-1", "ch-27") |

### Morning adhkar

```
GET /v1/azkar/morning
```

### Evening adhkar

```
GET /v1/azkar/evening
```

### Sleeping adhkar

```
GET /v1/azkar/sleeping
```

### Post-salah adhkar

```
GET /v1/azkar/post-salah
```

### Search adhkar

```
GET /v1/azkar/search?q={text}&lang={lang}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query (min 2 chars) |
| `lang` | string | `ar` | Language: `ar` or `en` |
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page (1-100) |

---

## Tafsir

### List books

```
GET /v1/tafsir/books
```

Available tafsirs: qurtubi, ibn-kathir, baghawi, saadi

### Get tafsir for a surah

```
GET /v1/tafsir/{book}/{surah}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `book` | string | Tafsir book ID |
| `surah` | int | Surah number |

### Get tafsir for an ayah

```
GET /v1/tafsir/{book}/{surah}/{ayah}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `book` | string | Tafsir book ID |
| `surah` | int | Surah number |
| `ayah` | int | Ayah number |

### Search tafsir

```
GET /v1/tafsir/{book}/search?q={text}
```

---

## Prayer Times

### Get prayer times

```
GET /v1/prayer/times?city={city}
GET /v1/prayer/times?lat={lat}&lon={lon}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `city` | string | City name |
| `lat` | float | Latitude |
| `lon` | float | Longitude |

### List cities

```
GET /v1/prayer/cities?q={search}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Optional search filter |

---

## Audio

### Radio stations

```
GET /v1/audio/stations?page={page}&per_page={per_page}
```

### Reciters

```
GET /v1/audio/reciters
```

---

## Duas

### List books

```
GET /v1/duas/books
```

### Get a book

```
GET /v1/duas/{bookId}
```

### Search duas

```
GET /v1/duas/search?q={text}
```

---

## Health Check

```
GET /health
```

Returns `{"status": "ok", "version": "1.0.0"}`.

## API Info

```
GET /v1
```

Returns API metadata, available endpoints, and dataset statistics.
