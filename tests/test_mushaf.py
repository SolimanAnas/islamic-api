"""Tests for mushaf (pages, images, fonts, coordinates) endpoints."""

import pytest


class TestMushafVersions:
    def test_list_versions(self, client):
        resp = client.get("/v1/mushaf/versions")
        assert resp.status_code == 200
        data = resp.json()["versions"]
        assert len(data) == 6
        ids = [v["id"] for v in data]
        assert "madina-1421" in ids
        assert "tajweed-colored" in ids

    def test_version_has_fields(self, client):
        resp = client.get("/v1/mushaf/versions")
        v = resp.json()["versions"][0]
        assert "id" in v
        assert "name" in v
        assert "format" in v
        assert "description" in v


class TestMushafPage:
    def test_get_page(self, client):
        resp = client.get("/v1/mushaf/madina-1421/page/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert data["version"] == "madina-1421"
        assert "image_url" in data
        assert "madina-1421/001.webp" in data["image_url"]

    def test_page_has_coordinates(self, client):
        resp = client.get("/v1/mushaf/madina-1421/page/1")
        data = resp.json()
        assert data["coordinates"] is not None
        assert data["coordinates"]["surah"] == 1

    def test_page_invalid_number(self, client):
        resp = client.get("/v1/mushaf/madina-1421/page/0")
        assert resp.status_code == 400

    def test_page_too_high(self, client):
        resp = client.get("/v1/mushaf/madina-1421/page/605")
        assert resp.status_code == 400

    def test_unknown_version(self, client):
        resp = client.get("/v1/mushaf/fake-version/page/1")
        assert resp.status_code == 400

    def test_tajweed_page_format(self, client):
        resp = client.get("/v1/mushaf/tajweed-colored/page/1")
        assert resp.status_code == 200
        assert ".webp" in resp.json()["image_url"]

    def test_png_version(self, client):
        resp = client.get("/v1/mushaf/mushaf-1024/page/1")
        assert resp.status_code == 200
        assert ".png" in resp.json()["image_url"]


class TestMushafLines:
    def test_get_page_lines(self, client):
        resp = client.get("/v1/mushaf/page/1/lines")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert "lines" in data
        assert len(data["lines"]) > 0

    def test_line_has_image_url(self, client):
        resp = client.get("/v1/mushaf/page/1/lines")
        lines = resp.json()["lines"]
        first_line = list(lines.values())[0]
        assert "image_url" in first_line
        assert "line-by-line/1/" in first_line["image_url"]

    def test_line_has_ayah_mapping(self, client):
        resp = client.get("/v1/mushaf/page/1/lines")
        lines = resp.json()["lines"]
        has_ayah = any("surah" in v for v in lines.values())
        assert has_ayah

    def test_get_single_line(self, client):
        resp = client.get("/v1/mushaf/page/1/line/6")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert data["line"] == 6
        assert "image_url" in data

    def test_line_not_found(self, client):
        resp = client.get("/v1/mushaf/page/1/line/9")
        assert resp.status_code == 404

    def test_line_invalid_number(self, client):
        resp = client.get("/v1/mushaf/page/1/line/0")
        assert resp.status_code == 400

    def test_page_lines_invalid(self, client):
        resp = client.get("/v1/mushaf/page/0/lines")
        assert resp.status_code == 400


class TestMushafFont:
    def test_get_font(self, client):
        resp = client.get("/v1/mushaf/font/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert "font_url" in data
        assert "p1.woff2" in data["font_url"]
        assert data["format"] == "woff2"

    def test_font_invalid_page(self, client):
        resp = client.get("/v1/mushaf/font/0")
        assert resp.status_code == 400


class TestAyahLocation:
    def test_find_ayah_location(self, client):
        resp = client.get("/v1/mushaf/ayah-location/1/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["surah"] == 1
        assert data["ayah"] == 1
        assert data["page"] is not None
        assert data["line"] is not None
        assert "line_image_url" in data

    def test_ayah_location_invalid_surah(self, client):
        resp = client.get("/v1/mushaf/ayah-location/999/1")
        assert resp.status_code == 400

    def test_ayah_location_ayah_invalid(self, client):
        resp = client.get("/v1/mushaf/ayah-location/1/999")
        assert resp.status_code == 400
