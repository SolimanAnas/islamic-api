import pytest


class TestPrayerCities:
    def test_list_cities(self, client):
        response = client.get("/v1/prayer/cities")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] > 0

    def test_city_has_fields(self, client):
        response = client.get("/v1/prayer/cities")
        city = response.json()["data"][0]
        assert "name" in city
        assert "lat" in city
        assert "lng" in city

    def test_search_cities(self, client):
        response = client.get("/v1/prayer/cities?q=Cairo")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0


class TestPrayerTimes:
    def test_missing_params(self, client):
        response = client.get("/v1/prayer/times")
        assert response.status_code == 400


class TestAudio:
    def test_list_stations(self, client):
        response = client.get("/v1/audio/stations")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) > 0

    def test_list_reciters(self, client):
        response = client.get("/v1/audio/reciters")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] > 0


class TestDuas:
    def test_list_books(self, client):
        response = client.get("/v1/duas/books")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 5

    def test_get_book(self, client):
        response = client.get("/v1/duas/book-1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "items" in data
        assert len(data["items"]) > 0

    def test_book_not_found(self, client):
        response = client.get("/v1/duas/nonexistent")
        assert response.status_code == 404

    def test_search_duas(self, client):
        response = client.get("/v1/duas/search?q=اللهم")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestHealthAndInfo:
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_api_info(self, client):
        response = client.get("/v1")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "stats" in data
