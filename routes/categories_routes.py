from flask import Blueprint, jsonify
from services.scraper import scrape_categories
from services.storage import read_json, write_json

# Blueprint för category-routes
categories_bp = Blueprint("categories_bp", __name__)

# Var vi lagrar kategorierna i JSON
CATEGORIES_PATH = "data/categories.json"


@categories_bp.get("/api/v1/categories")
def get_categories():
    """
    GET /api/v1/categories
    - Om categories.json finns och innehåller data: returnera den
    - Annars: scrapa kategorier, spara i categories.json och returnera
    """
    cats = read_json(CATEGORIES_PATH, default=[])

    # Om filen är tom ([]) eller saknas => scrapa på nytt
    if not cats:
        cats = scrape_categories()
        write_json(CATEGORIES_PATH, cats)

    return jsonify(cats)