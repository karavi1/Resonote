from bs4 import BeautifulSoup
import re

def clean_html(raw_html: str) -> str:
    """
    Remove ads, popups, and extraneous HTML from content. Returns clean text.
    """
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove script, style, and hidden elements
    for tag in soup(["script", "style", "noscript", "footer", "header", "nav", "aside"]):
        tag.decompose()

    # Common annoying classes/ids (ads, popups, cookie notices)
    annoying_keywords = ["cookie", "popup", "banner", "ad", "subscribe", "newsletter"]
    for attr in ["class", "id"]:
        for keyword in annoying_keywords:
            for tag in soup.find_all(attrs={attr: re.compile(keyword, re.I)}):
                tag.decompose()

    # Get text content, preserve simple structure
    cleaned_text = soup.get_text(separator="\n", strip=True)

    # Collapse extra newlines
    cleaned_text = re.sub(r'\n{2,}', '\n\n', cleaned_text)

    return cleaned_text
