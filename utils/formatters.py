def format_rating(rating):
    if rating is None:
        return "—"
    try:
        return f"{float(rating):.1f}"
    except (ValueError, TypeError):
        return "—"

def format_movie(movie: dict) -> tuple[str, str | None]:
    title = movie.get("name", "Без названия")
    year = movie.get("year", "—")
    rating = format_rating(movie.get("rating", {}).get("kp"))
    description = movie.get("description", "Описание отсутствует")

    text = f"<b>{title}</b> ({year})\n"
    text += f"⭐ <b>Рейтинг КП:</b> {rating}\n\n"
    text += description

    poster = movie.get("poster", {}).get("url")

    return text, poster
