import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8443877498:AAFDoZSnzzQksrEHESwlj6qqQ2aFiK60JSs")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY", "AD79R6V-26WM6Y5-PJTYAYC-D3SF1HG")

KINOPOISK_API_URL = "https://api.poiskkino.dev/v1.4"

GENRES = [
    "комедия", "драма", "боевик", "фантастика", "ужасы",
    "триллер", "мелодрама", "детектив", "приключения",
    "фэнтези", "мультфильм", "криминал"
]
