import pytest


class TestHisnMuslim:
    def test_list_chapters(self, client):
        response = client.get("/v1/azkar/hisn/chapters")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 132

    def test_chapter_has_fields(self, client):
        response = client.get("/v1/azkar/hisn/chapters")
        ch = response.json()["data"][0]
        assert "id" in ch
        assert "title" in ch
        assert "items_count" in ch

    def test_get_chapter(self, client):
        response = client.get("/v1/azkar/hisn/ch-1")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "items" in data
        assert len(data["items"]) > 0

    def test_chapter_not_found(self, client):
        response = client.get("/v1/azkar/hisn/nonexistent")
        assert response.status_code == 404


class TestAzkarCategories:
    def test_morning(self, client):
        response = client.get("/v1/azkar/morning")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] > 0

    def test_evening(self, client):
        response = client.get("/v1/azkar/evening")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] > 0

    def test_sleeping(self, client):
        response = client.get("/v1/azkar/sleeping")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] > 0

    def test_post_salah(self, client):
        response = client.get("/v1/azkar/post-salah")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestAzkarSearch:
    def test_search(self, client):
        response = client.get("/v1/azkar/search?q=الله&lang=ar")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) > 0

    def test_search_too_short(self, client):
        response = client.get("/v1/azkar/search?q=a")
        assert response.status_code == 422
