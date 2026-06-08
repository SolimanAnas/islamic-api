import pytest


class TestQuranSurahs:
    def test_list_surahs(self, client):
        response = client.get("/v1/quran/surahs")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 114

    def test_surah_has_required_fields(self, client):
        response = client.get("/v1/quran/surahs")
        surah = response.json()["data"][0]
        assert "number" in surah
        assert "name_ar" in surah
        assert "name_en" in surah
        assert "ayah_count" in surah

    def test_surah_al_fatiha(self, client):
        response = client.get("/v1/quran/surah/1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["number"] == 1
        assert data["ayah_count"] == 7
        assert len(data["ayahs"]) == 7

    def test_surah_al_baqarah(self, client):
        response = client.get("/v1/quran/surah/2")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["number"] == 2
        assert data["ayah_count"] == 286

    def test_surah_not_found(self, client):
        response = client.get("/v1/quran/surah/999")
        assert response.status_code == 404

    def test_surah_invalid_range(self, client):
        response = client.get("/v1/quran/surah/0")
        assert response.status_code == 404


class TestQuranAyah:
    def test_get_ayah(self, client):
        response = client.get("/v1/quran/ayah/1/1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["surah"] == 1
        assert data["ayah"] == 1
        assert "text_uthmani" in data

    def test_ayah_not_found(self, client):
        response = client.get("/v1/quran/ayah/1/999")
        assert response.status_code == 404


class TestQuranJuz:
    def test_get_juz_1(self, client):
        response = client.get("/v1/quran/juz/1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["juz"] == 1
        assert data["ayah_count"] > 0
        assert len(data["ayahs"]) > 0

    def test_juz_invalid(self, client):
        response = client.get("/v1/quran/juz/31")
        assert response.status_code == 400


class TestQuranSearch:
    def test_search_arabic(self, client):
        response = client.get("/v1/quran/search?q=الرحمن&lang=ar")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) > 0

    def test_search_too_short(self, client):
        response = client.get("/v1/quran/search?q=a")
        assert response.status_code == 422
