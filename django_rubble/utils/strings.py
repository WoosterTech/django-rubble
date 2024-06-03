def sort_title(title: str) -> str:
    """Sort a title by the first word, ignoring articles."""
    articles = {"a", "an", "the"}

    title = title.lower()

    first, _, rest = title.partition(" ")
    return f"{rest}, {first}" if first in articles else title
