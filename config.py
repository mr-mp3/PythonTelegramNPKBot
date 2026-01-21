import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "...")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY", "...")

KINOPOISK_API_URL = "https://api.poiskkino.dev/v1.4"

GENRES = [
    "комедия", "драма", "боевик", "фантастика", "ужасы",
    "триллер", "мелодрама", "детектив", "приключения",
    "фэнтези", "мультфильм", "криминал"
]
