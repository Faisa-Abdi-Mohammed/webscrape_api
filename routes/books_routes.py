from flask import Blueprint, jsonify, request
from datetime import datetime

from services.storage import read_json, write_json
from services.scraper import scrape_books_in_category
from services.currency import get_gbp_sek_rate, gbp_to_sek

books_bp = Blueprint("books_bp", __name__)


def _today_stamp() -> str:
    return datetime.now().strftime("%Y%m%d")


def _file_path_for_category(category: str) -> str:
    return f"data/books/{category.lower()}_{_today_stamp()}.json"


def _get_category_url(category: str) -> str | None:
    categories = read_json("data/categories.json", default=[])
    category_lower = category.lower()

    for c in categories:
        if c.get("name", "").lower() == category_lower:
            return c.get("url")
    return None


@books_bp.get("/api/v1/books/<category>")
def get_books(category: str):
    category_url = _get_category_url(category)
    if not category_url:
        return jsonify({"error": f"Category '{category}' not found. Run /api/v1/categories first."}), 404

    path = _file_path_for_category(category)

    # Använd dagens fil om den finns
    data = read_json(path, default=None)
    if data is not None:
        return jsonify(data), 200

    # Annars scrapa
    books = scrape_books_in_category(category_url)

    # Lägg till SEK-pris
    rate = get_gbp_sek_rate()
    for b in books:
        b["price_sek"] = gbp_to_sek(b["price_gbp"], rate)

    write_json(path, books)
    return jsonify(books), 200


@books_bp.post("/api/v1/books/<category>")
def add_book(category: str):
    path = _file_path_for_category(category)
    books = read_json(path, default=None)

    if books is None:
        return jsonify({"error": "Category file not found. Run GET first to create today's file."}), 404

    new_data = request.get_json()
    if not new_data:
        return jsonify({"error": "No JSON body provided"}), 400

    title = new_data.get("title")
    price_gbp = new_data.get("price_gbp")
    rating = new_data.get("rating")

    if title is None or price_gbp is None or rating is None:
        return jsonify({"error": "Missing fields. Required: title, price_gbp, rating"}), 400

    new_id = max([b.get("id", 0) for b in books], default=0) + 1

    # Beräkna SEK automatiskt
    rate_value = get_gbp_sek_rate()
    price_sek = gbp_to_sek(float(price_gbp), rate_value)

    new_book = {
        "id": new_id,
        "title": title,
        "price_gbp": float(price_gbp),
        "price_sek": price_sek,
        "rating": int(rating),
    }

    books.append(new_book)
    write_json(path, books)

    return jsonify(new_book), 201


@books_bp.put("/api/v1/books/<category>/<int:book_id>")
def update_book(category: str, book_id: int):
    path = _file_path_for_category(category)
    books = read_json(path, default=None)

    if books is None:
        return jsonify({"error": "Category file not found. Run GET first."}), 404

    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No JSON body provided"}), 400

    book = next((b for b in books if b.get("id") == book_id), None)
    if book is None:
        return jsonify({"error": f"Book with id {book_id} not found"}), 404

    if "title" in update_data:
        book["title"] = update_data["title"]

    if "rating" in update_data:
        book["rating"] = int(update_data["rating"])

    if "price_gbp" in update_data:
        book["price_gbp"] = float(update_data["price_gbp"])
        # Om GBP ändras -> uppdatera SEK automatiskt
        rate_value = get_gbp_sek_rate()
        book["price_sek"] = gbp_to_sek(book["price_gbp"], rate_value)

    write_json(path, books)
    return jsonify(book), 200


@books_bp.delete("/api/v1/books/<category>/<int:book_id>")
def delete_book(category: str, book_id: int):
    path = _file_path_for_category(category)
    books = read_json(path, default=None)

    if books is None:
        return jsonify({"error": "Category file not found. Run GET first."}), 404

    book = next((b for b in books if b.get("id") == book_id), None)
    if book is None:
        return jsonify({"error": f"Book with id {book_id} not found"}), 404

    books = [b for b in books if b.get("id") != book_id]
    write_json(path, books)

    return jsonify({"message": f"Book {book_id} deleted successfully"}), 200