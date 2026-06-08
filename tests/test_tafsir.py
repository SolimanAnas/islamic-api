import pytest


class TestTafsirBooks:
    def test_list_books(self, client):
        response = client.get("/v1/tafsir/books")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 4

    def test_book_has_fields(self, client):
        response = client.get("/v1/tafsir/books")
        book = response.json()["data"][0]
        assert "id" in book
        assert "name" in book
        assert "available" in book


class TestTafsirContent:
    def test_get_surah_tafsir(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] > 0

    def test_get_ayah_tafsir(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/1/1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "Tafsir" in data or "text" in data

    def test_tafsir_not_found(self, client):
        response = client.get("/v1/tafsir/nonexistent/1")
        assert response.status_code == 404

    def test_ayah_not_found(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/1/9999")
        assert response.status_code == 404


class TestTafsirSearch:
    def test_search(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/search?q=الله")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_search_too_short(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/search?q=a")
        assert response.status_code == 422


class TestTafsirSQLInjection:
    """Security tests for SQLite queries."""

    def test_sql_injection_surah(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/1%20OR%201=1")
        assert response.status_code in [400, 404, 422]

    def test_sql_injection_search(self, client):
        response = client.get("/v1/tafsir/ibn-kathir/search?q='; DROP TABLE tafsir; --")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
