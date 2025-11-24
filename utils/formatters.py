def format_rating(rating):
    """Форматирует рейтинг, скрывая нулевые значения"""
    if not rating or rating == 0 or rating == '0' or rating == '0.0':
        return None
    try:
        return float(rating)
    except (ValueError, TypeError):
        return None


def format_movie_info(movie):
    """Форматирует информацию о фильме для отправки"""
    title = movie.get('name', 'Название не указано')
    year = movie.get('year', 'Год не указан')
    description = movie.get('description', 'Описание отсутствует')

    # Проверяем, что description не None перед получением длины
    if description and len(description) > 500:
        description = description[:500] + '...'

    # Рейтинги
    rating = movie.get('rating', {})
    kp_rating = format_rating(rating.get('kp'))
    imdb_rating = format_rating(rating.get('imdb'))

    # Жанры и страны
    genres = [genre.get('name', '') for genre in movie.get('genres', [])]
    countries = [country.get('name', '') for country in movie.get('countries', [])]

    movie_length = movie.get('movieLength', 'Не указана')
    age_rating = movie.get('ageRating', 'Не указан')

    # Формируем ответ
    response_text = f"🎬 <b>{title}</b> ({year})\n\n"

    if kp_rating:
        response_text += f"⭐ Рейтинг КП: <b>{kp_rating}</b>\n"
    if imdb_rating:
        response_text += f"⭐ Рейтинг IMDb: <b>{imdb_rating}</b>\n"

    response_text += f"""
🎭 Жанры: {', '.join(genres) if genres else 'Не указаны'}
🌍 Страны: {', '.join(countries) if countries else 'Не указаны'}
⏱ Длительность: {movie_length} мин
🔞 Возрастной рейтинг: {age_rating}

📖 {description}
    """.strip()

    poster_url = movie.get('poster', {}).get('url')

    return response_text, poster_url