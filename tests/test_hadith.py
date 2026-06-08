import pytest


class TestHadithCollections:
    def test_list_collections(self, client):
        response = client.get("/v1/hadith/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 13

    def test_collection_has_required_fields(self, client):
        response = client.get("/v1/hadith/collections")
        col = response.json()["data"][0]
        assert "id" in col
        assert "name_ar" in col
        assert "name_en" in col
        assert "total_hadith" in col


class TestHadithCollection:
    def test_get_bukhari(self, client):
        response = client.get("/v1/hadith/bukhari")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == "bukhari"
        assert data["data"]["total_hadith"] > 0

    def test_get_muslim(self, client):
        response = client.get("/v1/hadith/muslim")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == "muslim"

    def test_collection_not_found(self, client):
        response = client.get("/v1/hadith/nonexistent")
        assert response.status_code == 404

    def test_pagination(self, client):
        response = client.get("/v1/hadith/bukhari?page=1&per_page=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["hadiths"]) == 5
        assert data["meta"]["page"] == 1
        assert data["meta"]["per_page"] == 5


class TestHadithItem:
    def test_get_hadith(self, client):
        response = client.get("/v1/hadith/nawawi40/1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "arabic" in data or "english" in data or "text" in data

    def test_hadith_not_found(self, client):
        response = client.get("/v1/hadith/bukhari/999999")
        assert response.status_code == 404


class TestHadithSearch:
    def test_search(self, client):
        response = client.get("/v1/hadith/search?q=prayer&lang=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_search_too_short(self, client):
        response = client.get("/v1/hadith/search?q=a")
        assert response.status_code == 422


class TestHadithRandom:
    def test_random_hadith(self, client):
        response = client.get("/v1/hadith/random/nawawi40")
        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, dict)
