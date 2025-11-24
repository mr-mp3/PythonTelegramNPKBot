import os


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8443877498:AAFDoZSnzzQksrEHESwlj6qqQ2aFiK60JSs')
    KINOPOISK_API_KEY = os.getenv('KINOPOISK_API_KEY', 'C0VEPJ3-0J24GPR-GEJX8RP-6TA66FK')
    KINOPOISK_API_URL = 'https://api.kinopoisk.dev/v1.4'

    GENRES = [
        "комедия", "драма", "боевик", "фантастика", "ужасы", "триллер",
        "мелодрама", "детектив", "приключения", "фэнтези", "мультфильм",
        "биография", "история", "криминал", "вестерн", "военный"
    ]