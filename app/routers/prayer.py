from fastapi import APIRouter, Query, HTTPException

from app.services.data_loader import get_store

router = APIRouter()


@router.get("/cities", summary="List available cities for prayer times")
def list_cities(
    q: str | None = Query(None, description="Search city name"),
):
    store = get_store()
    cities = [
        {"name": name, "lat": coords.get("lat", 0), "lng": coords.get("lng", 0)}
        for name, coords in store.cities.items()
    ]
    if q:
        cities = [c for c in cities if q.lower() in c["name"].lower()]
    return {"success": True, "data": cities, "count": len(cities)}


@router.get("/times", summary="Get prayer times for a city or coordinates")
async def get_prayer_times(
    city: str | None = Query(None, description="City name"),
    lat: float | None = Query(None, description="Latitude"),
    lon: float | None = Query(None, description="Longitude"),
):
    import httpx
    from datetime import date

    today = date.today()
    date_str = f"{today.day}-{today.month}-{today.year}"

    if lat and lon:
        url = f"https://api.aladhan.com/v1/timings/{date_str}?latitude={lat}&longitude={lon}"
    elif city:
        store = get_store()
        coords = store.cities.get(city)
        if coords:
            url = f"https://api.aladhan.com/v1/timings/{date_str}?latitude={coords['lat']}&longitude={coords['lng']}"
        else:
            url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?city={city}"
    else:
        raise HTTPException(status_code=400, detail="Provide 'city' or 'lat'+'lon' parameters")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            data = response.json()
            if data.get("code") == 200:
                timings = data["data"]["timings"]
                return {
                    "success": True,
                    "data": {
                        "fajr": timings.get("Fajr"),
                        "sunrise": timings.get("Sunrise"),
                        "dhuhr": timings.get("Dhuhr"),
                        "asr": timings.get("Asr"),
                        "maghrib": timings.get("Maghrib"),
                        "isha": timings.get("Isha"),
                        "sunset": timings.get("Sunset"),
                    },
                    "date": date_str,
                    "city": city or f"{lat},{lon}",
                }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Prayer times API error: {str(e)}")

    raise HTTPException(status_code=502, detail="Failed to fetch prayer times")
