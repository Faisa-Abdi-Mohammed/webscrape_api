import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def scrape_categories() -> List[Dict[str, str]]:
    response = requests.get(BASE_URL, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    categories = []
    for a in soup.select(".side_categories ul li ul li a"):
        categories.append({
            "name": a.get_text(strip=True),
            "url": urljoin(BASE_URL, a.get("href"))
        })
    return categories


def _extract_rating(star_tag) -> int:
    # Rating finns som class: "star-rating Three"
    if not star_tag:
        return 0
    for c in star_tag.get("class", []):
        if c in RATING_MAP:
            return RATING_MAP[c]
    return 0


def _clean_price_to_float(price_text: str) -> float:
    # Tar bort konstiga tecken med regex
    cleaned = re.sub(r"[^\d.]", "", price_text)
    return float(cleaned) if cleaned else 0.0


def scrape_books_in_category(category_url: str) -> list[dict]:
    books: list[dict] = []
    page_url = category_url

    while True:
        resp = requests.get(page_url, timeout=20)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        for article in soup.select("article.product_pod"):
            title = article.select_one("h3 a").get("title", "").strip()
            price_text = article.select_one(".price_color").get_text(strip=True)

            books.append({
                "id": len(books) + 1,
                "title": title,
                "price_gbp": _clean_price_to_float(price_text),
                "rating": _extract_rating(article.select_one(".star-rating"))
            })

        next_link = soup.select_one("li.next a")
        if not next_link:
            break

        page_url = urljoin(page_url, next_link.get("href"))

    return books