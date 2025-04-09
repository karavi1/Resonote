import re
from urllib.parse import urlparse

def extract_metadata(source_url: str, title: str = None) -> dict:
    """
    Extract metadata from a URL and optional title. No content parsing.
    """
    parsed = urlparse(source_url)
    path_parts = [part for part in parsed.path.strip("/").split("/") if part]

    # Use provided title or generate from URL
    fallback_title = re.sub(r"[-_/]+", " ", path_parts[-1]).title() if path_parts else parsed.netloc
    final_title = title or fallback_title

    # Basic tag extraction from URL path
    tags = [part.lower() for part in path_parts if part.isalpha() and len(part) > 2]

    return {
        "title": final_title,
        "author": None,
        "estimated_reading_time_min": 3,  # Default value
        "tags": tags[:5],
        "source_url": source_url,
    }