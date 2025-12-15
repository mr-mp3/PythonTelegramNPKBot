import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8443877498:AAFDoZSnzzQksrEHESwlj6qqQ2aFiK60JSs")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY", "TCPD5P5-X794MKP-GKFBCMT-08107MS")

KINOPOISK_API_URL = 'https://api.kinopoisk.dev/v1.4'

GENRES = [
    "комедия", "драма", "боевик", "фантастика", "ужасы",
    "триллер", "мелодрама", "детектив", "приключения",
    "фэнтези", "мультфильм", "криминал"
]
