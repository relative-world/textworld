import re

import unicodedata


def slugify(name: str) -> str:
    """Convert a string to a valid filename."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()
