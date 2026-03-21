## Lightweight Python Backend

This repo now includes a minimal sample backend for a restaurant review web app, built with the Python standard library.

### Run it

```bash
python3 -m app.main
```

The server starts on `http://127.0.0.1:8000` by default.

### Endpoints

- `GET /health` returns a simple health check
- `GET /restaurants` lists restaurants and supports filtering
- `GET /restaurants/<restaurant_id>` returns one restaurant
- `POST /restaurants` creates a restaurant
- `POST /restaurants/<restaurant_id>/reviews` creates a review
- `POST /seed` loads a small demo dataset
- `POST /reset` clears the in-memory data

`GET /restaurants` supports these optional query params:

- `cuisine=Japanese`
- `location=Toronto`
- `min_rating=4`
- `sort=name|rating|reviews`

### Example requests

```bash
curl -X POST http://127.0.0.1:8000/seed
curl http://127.0.0.1:8000/restaurants
curl "http://127.0.0.1:8000/restaurants?location=Toronto&min_rating=4&sort=rating"
curl -X POST http://127.0.0.1:8000/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name":"Cafe Juniper","cuisine":"Cafe","location":"Montreal","price_range":"$$"}'
```
