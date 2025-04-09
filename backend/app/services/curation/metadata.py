import re
import math
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_metadata(cleaned_text: str, source_url: str) -> dict:
    """
    Extract title, author, estimated reading time, and basic topic tags (placeholder).
    """
    # Placeholder title guess (can be improved later)
    lines = cleaned_text.splitlines()
    title = lines[0] if lines else "Untitled"

    # Placeholder author detection (optional enhancement)
    author = None
    for line in lines[:10]:
        if re.search(r'by\s+[A-Z][a-z]+', line, re.I):
            author = line.strip()
            break

    # Word count and estimated reading time
    word_count = len(re.findall(r'\w+', cleaned_text))
    reading_time_minutes = math.ceil(word_count / 200)  # ~200 wpm estimate TODO: Replace as a constant that we can have updated (manually or learned?)

    # Basic tags (can be expanded later with NLP)
    tags = extract_basic_tags(source_url)

    return {
        "title": title,
        "author": author,
        "estimated_reading_time_min": reading_time_minutes,
        "tags": tags,
        "source_url": source_url
    }

def extract_basic_tags(url: str) -> list:
    """
    Extract rough topic tags from URL path or domain.
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    tags = [part for part in path_parts if part and len(part) < 20]
    return list(set(tags))
