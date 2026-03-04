from flask import Flask, jsonify
from routes.categories_routes import categories_bp
from routes.books_routes import books_bp

app = Flask(__name__)

# Startsida
@app.get("/")
def home():
    return jsonify({
        "message": "API is running",
        "try": [
            "/api/v1/health",
            "/api/v1/categories",
            "/api/v1/books/travel"
        ]
    })

# Health-check
@app.get("/api/v1/health")
def health():
    return jsonify({"status": "ok"})

# Blueprints
app.register_blueprint(categories_bp)
app.register_blueprint(books_bp)

if __name__ == "__main__":
    app.run(debug=True)