from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.services.data_loader import load_all_data

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_all_data()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent.parent / "index.html"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    if INDEX_PATH.exists():
        return HTMLResponse(content=INDEX_PATH.read_text(encoding="utf-8"))
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok", "version": settings.APP_VERSION, "index_exists": INDEX_PATH.exists(), "index_path": str(INDEX_PATH)}


@app.get("/v1")
def api_info():
    from app.services.data_loader import get_store
    store = get_store()
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "endpoints": {
            "quran": "/v1/quran",
            "hadith": "/v1/hadith",
            "azkar": "/v1/azkar",
            "tafsir": "/v1/tafsir",
            "prayer": "/v1/prayer",
            "audio": "/v1/audio",
            "duas": "/v1/duas",
        },
        "stats": {
            "quran_surahs": len(store.quran_surahs),
            "hadith_collections": len(store.hadith_collections),
            "hisn_chapters": len(store.hisn_chapters),
            "azkar_morning": len(store.azkar_morning),
            "azkar_evening": len(store.azkar_evening),
            "azkar_sleeping": len(store.azkar_sleeping),
            "radio_stations": len(store.radio_stations),
            "reciters": len(store.reciters),
        },
    }


from app.routers import quran, hadith, azkar, tafsir, prayer, audio, duas

app.include_router(quran.router, prefix="/v1/quran", tags=["Quran"])
app.include_router(hadith.router, prefix="/v1/hadith", tags=["Hadith"])
app.include_router(azkar.router, prefix="/v1/azkar", tags=["Adhkar"])
app.include_router(tafsir.router, prefix="/v1/tafsir", tags=["Tafsir"])
app.include_router(prayer.router, prefix="/v1/prayer", tags=["Prayer"])
app.include_router(audio.router, prefix="/v1/audio", tags=["Audio"])
app.include_router(duas.router, prefix="/v1/duas", tags=["Duas"])
