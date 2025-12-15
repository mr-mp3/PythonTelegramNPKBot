def format_movie(movie: dict):
    title = movie.get("name", "Без названия")
    year = movie.get("year", "")
    rating = movie.get("rating", {}).get("kp")
    description = movie.get("description", "Описание отсутствует")[:400]

    text = (
        f"🎬 <b>{title}</b> ({year})\n"
        f"⭐ Рейтинг КП: {rating}\n\n"
        f"{description}"
    )

    poster = movie.get("poster", {}).get("url")
    return text, poster
