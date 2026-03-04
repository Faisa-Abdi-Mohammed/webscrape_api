# Web scraping API - Flask
Detta projekt är ett REST API byggt med Flask som scrapear bokdata från webbplatsen: https://books.toscrape.com

API:t hämtar bokkategorier och böcker från sidan, spara data i JSON-filer och gör det möjligt att utföra CRUD-operationer.

## Funktioner
- Web scraping med **requests** och **BeautifulSoup**
- Data sparas i **JSON-filer**
- **Cache-logik** baserat på datum
- **CRUD-operationer** (GET, POST, PUT, DELETE)
- Pris konverteras från **GBP till SEK**
- REST API byggt med **Flask**
- Deployment på **PythonAnywhere**

- ## API Endpoints

GET /api/v1/health  
GET /api/v1/categories  
GET /api/v1/books/<kategori>

POST /api/v1/books/<kategori>  
PUT /api/v1/books/<kategori>/<id>  
DELETE /api/v1/books/<kategori>/<id>

## Live API (PythonAnywhere)

API:t är deployat och kan testas här:
https://faisaabdi566.pythonanywhere.com/api/v1/health
