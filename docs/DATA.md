# Data Sources & Attribution

## Quran

| Field | Value |
|-------|-------|
| **Script** | Uthmani (verified) |
| **Ayahs** | 6,236 |
| **Surahs** | 114 |
| **Source** | [quran.com](https://quran.com) API |
| **File** | `data/quran/quran.json` |

Each ayah includes: `surah`, `ayah`, `text_uthmani`, `text_clean`, `surah_name`, `surah_name_en`.

---

## Hadith Collections

All hadith are sourced from [sunnah.com](https://sunnah.com) verified databases.

| Collection | Arabic Name | Hadith Count | Sections |
|------------|-------------|-------------|----------|
| Sahih al-Bukhari | صحيح البخاري | ~7,563 | 97 |
| Sahih Muslim | صحيح مسلم | ~5,363 | — |
| Sunan Abu Dawud | سنن أبي داود | ~4,590 | 43 |
| Jami at-Tirmidhi | جامع الترمذي | ~3,956 | 48 |
| Sunan an-Nasa'i | سنن النسائي | ~5,095 | 51 |
| Sunan Ibn Majah | سنن ابن ماجه | ~4,341 | 38 |
| Mishkat al-Masabih | مشكاة المصابيح | ~4,428 | 30 |
| Riyad as-Salihin | رياض الصالحين | ~1,896 | 18 |
| Bulugh al-Maram | بُلُوغ المرام | ~1,767 | 16 |
| Al-Adab Al-Mufrad | الأدب المفرد | ~1,326 | — |
| Shama'il Muhammadiyah | الشمائل المحمدية | ~402 | — |
| 40 Hadith Qudsi | أربعون حديثاً قدسياً | 40 | — |
| 40 Hadith Nawawi | الأربعون النووية | 42 | — |

Each hadith includes: Arabic text, English translation, narrator, section, grades.

---

## Adhkar (Remembrances)

### Hisn Muslim (Fortress of the Muslim)

| Field | Value |
|-------|-------|
| **Chapters** | 132 |
| **Author** | Dr. Said bin Wahf al-Qahtani |
| **Source** | [hisnmuslim.com](https://hisnmuslim.com) |
| **File** | `data/azkar/hisn.json` |

Each chapter includes: Arabic title, English title, audio URL, items with Arabic text, English translation, transliteration, repetition count, and audio.

### Morning & Evening Adhkar

| Field | Value |
|-------|-------|
| **Source** | Verified prophetic adhkar |
| **File** | `data/azkar/azkar.json` |

### Sleeping Adhkar

| Field | Value |
|-------|-------|
| **Source** | Verified prophetic adhkar |
| **File** | `data/azkar/sleeping.json` |

### Post-Salah Adhkar

| Field | Value |
|-------|-------|
| **Source** | Verified prophetic adhkar |
| **File** | `data/azkar/salah.json` |

---

## Duas (Supplications)

| Field | Value |
|-------|-------|
| **Books** | 5 |
| **Content** | Comprehensive prophetic duas |
| **Source** | Verified Islamic references |
| **Files** | `data/duas/duaa-01.json` to `duaa-05.json` |

---

## Tafsir (Quran Exegesis)

| Tafsir | Author | Language |
|--------|--------|----------|
| al-Qurtubi | Imam al-Qurtubi | Arabic |
| Ibn Kathir | Ibn Kathir | Arabic |
| al-Baghawi | Imam al-Baghawi | Arabic |
| as-Sa'di | Sheikh as-Sa'di | Arabic |

Stored as SQLite databases in `data/tafsir/`.

---

## Audio

### Radio Stations

| Field | Value |
|-------|-------|
| **Count** | 150+ |
| **Content** | Quran radio streaming stations |
| **File** | `data/audio/stations.json` |

### Reciters

| Field | Value |
|-------|-------|
| **Count** | 40+ |
| **Content** | Quran reciters with audio file mappings |
| **File** | `data/audio/reciters.json` |

---

## Prayer Times

| Field | Value |
|-------|-------|
| **API** | [aladhan.com](https://aladhan.com/prayer-time-api) |
| **Cities** | 200+ with coordinates |
| **Methods** | Multiple calculation methods |
| **File** | `data/prayer/cities.json` |

---

## License

All data is sourced from public Islamic references and is free to use. If you use this API in your project, attribution is appreciated but not required.

**Suggested attribution:**
> Islamic data powered by [Islamic API](https://github.com/SolimanAnas/islamic-api)
