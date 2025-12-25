import requests
from requests.exceptions import ReadTimeout, RequestException

from config import KINOPOISK_API_KEY, KINOPOISK_API_URL

HEADERS = {
    "X-API-KEY": KINOPOISK_API_KEY,
    "Content-Type": "application/json"
}


def search_movie(query: str, year: int | None = None, rating: float | None = None):
    """
    Поиск фильма по названию с учётом фильтров
    """
    try:
        params = {
            "query": query,
            "limit": 1,
            "selectFields": ["name", "year", "rating", "description", "poster"]
        }

        if year:
            params["year"] = f"{year}-2025"

        if rating:
            params["rating.kp"] = f"{rating}-10"

        response = requests.get(
            f"{KINOPOISK_API_URL}/movie/search",
            headers=HEADERS,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        movies = data.get("docs", [])

        if not movies:
            return None, "❌ Фильм не найден"

        return movies, None

    except ReadTimeout:
        return None, "⏳ Кинопоиск долго отвечает. Попробуйте ещё раз."

    except RequestException:
        return None, "❌ Ошибка соединения с Кинопоиском."


def is_valid_movie(movie: dict) -> bool:
    return (
        movie
        and movie.get("name")
        and movie.get("description")
        and movie.get("poster", {}).get("url")
        and movie.get("rating", {}).get("kp")
    )


def get_random_movie(max_attempts: int = 5):
    """
    Получает случайный КАЧЕСТВЕННЫЙ фильм
    """
    for _ in range(max_attempts):
        try:
            response = requests.get(
                f"{KINOPOISK_API_URL}/movie/random",
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()

            movie = response.json()

            if is_valid_movie(movie):
                return movie, None

        except ReadTimeout:
            return None, "⏳ Кинопоиск долго отвечает. Попробуйте ещё раз."
        except RequestException:
            continue

    return None, "😕 Не удалось найти хороший случайный фильм. Попробуйте ещё раз."

def get_top_movies(limit: int = 10):
    """
    Получает топ фильмов (Top-250)
    """
    try:
        response = requests.get(
            f"{KINOPOISK_API_URL}/movie",
            headers=HEADERS,
            params={
                "lists": "top250",
                "limit": limit,
                "selectFields": ["name", "year", "rating"]
            },
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        movies = data.get("docs", [])

        if not movies:
            return None, "❌ Не удалось загрузить топ фильмов"

        return movies, None

    except ReadTimeout:
        return None, "⏳ Кинопоиск долго отвечает. Попробуйте позже."

    except RequestException:
        return None, "❌ Ошибка соединения с Кинопоиском."
