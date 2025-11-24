import requests
import logging
from config import Config

logger = logging.getLogger(__name__)


class KinopoiskAPI:
    def __init__(self):
        self.config = Config()
        self.headers = {
            'X-API-KEY': self.config.KINOPOISK_API_KEY,
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, params=None):
        try:
            url = f"{self.config.KINOPOISK_API_URL}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=15)

            if response.status_code != 200:
                return None, f"❌ Ошибка API: {response.status_code}"

            return response.json(), None

        except Exception as e:
            logger.error(f"Ошибка API: {e}")
            return None, f"❌ Ошибка соединения"

    def _filter_movies(self, movies):
        """Фильтрует фильмы, убирая некорректные данные"""
        if not movies:
            return []

        filtered_movies = []
        for movie in movies:
            # Проверяем наличие названия и что оно не равно None/null
            title = movie.get('name')
            if not title or str(title).lower() in ['none', 'null', '']:
                continue

            # Проверяем наличие ID
            if not movie.get('id'):
                continue

            filtered_movies.append(movie)

        return filtered_movies

    def search_movies(self, query, limit=5):
        params = {
            'query': query,
            'limit': limit,
            'selectFields': ['id', 'name', 'year', 'description', 'rating', 'poster', 'genres', 'countries']
        }
        data, error = self._make_request('movie/search', params)

        # Фильтруем фильмы без названия
        if data and data.get('docs'):
            data['docs'] = self._filter_movies(data['docs'])

        return data, error

    def get_movie(self, movie_id):
        return self._make_request(f'movie/{movie_id}')

    def get_random_movie(self):
        return self._make_request('movie/random')

    def get_movies_by_genre(self, genre, page=1, limit=10):
        params = {
            'genres.name': genre,
            'limit': limit,
            'page': page,
            'selectFields': ['id', 'name', 'year', 'rating']
        }
        data, error = self._make_request('movie', params)

        # Фильтруем фильмы без названия
        if data and data.get('docs'):
            data['docs'] = self._filter_movies(data['docs'])

        return data, error

    def get_top_movies(self, limit=10):
        params = {
            'lists': 'top250',
            'limit': limit,
            'selectFields': ['id', 'name', 'year', 'rating']
        }
        data, error = self._make_request('movie', params)

        # Фильтруем фильмы без названия
        if data and data.get('docs'):
            data['docs'] = self._filter_movies(data['docs'])

        return data, error