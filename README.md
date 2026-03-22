# Restaurant Review Backend

This repo contains a lightweight sample Python backend for a restaurant review web app. It is intentionally small, dependency-free, and easy to use for demos, testing, and frontend integration work.

The API stores data in memory, exposes JSON endpoints over HTTP, and includes sample restaurant and review data for quick local testing.

## Features

- Standard-library-only backend with no external dependencies
- In-memory restaurant and review storage
- Restaurant creation and review submission
- Filtering by cuisine, location, and minimum rating
- Sorting by name, rating, or review count
- Featured restaurant recommendations
- Demo data seeding for fast local setup
- CORS headers enabled for local frontend development

## Quick Start

### Requirements

- Python 3.10 or newer

### Run the server

```bash
python3 -m app.main
```

By default, the server runs at `http://127.0.0.1:8000`.

You can also override the host and port:

```bash
HOST=0.0.0.0 PORT=9000 python3 -m app.main
```

## Project Structure

```text
app/
  __init__.py
  main.py              HTTP server and route handling
  recommendations.py   Featured restaurant ranking logic
  service.py           In-memory restaurant and review service
docs/
  api.md               Endpoint reference and example payloads
  architecture.md      Module responsibilities and request flow
  overview.md          High-level product and backend overview
README.md
requirements.txt
```

## API Summary

- `GET /health`
- `GET /restaurants`
- `GET /restaurants/featured`
- `GET /restaurants/<restaurant_id>`
- `POST /restaurants`
- `POST /restaurants/<restaurant_id>/reviews`
- `POST /seed`
- `POST /reset`

### Supported filters

`GET /restaurants` accepts these optional query parameters:

- `cuisine=Japanese`
- `location=Toronto`
- `min_rating=4`
- `sort=name|rating|reviews`

`GET /restaurants/featured` accepts:

- `limit=3`
- `price_range=$$`

## Example Usage

### Seed demo data

```bash
curl -X POST http://127.0.0.1:8000/seed
```

### List restaurants

```bash
curl http://127.0.0.1:8000/restaurants
```

### Filter restaurants

```bash
curl "http://127.0.0.1:8000/restaurants?location=Toronto&min_rating=4&sort=rating"
```

### Get featured restaurants

```bash
curl "http://127.0.0.1:8000/restaurants/featured?limit=2&price_range=$$"
```

### Create a restaurant

```bash
curl -X POST http://127.0.0.1:8000/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name":"Cafe Juniper","cuisine":"Cafe","location":"Montreal","price_range":"$$"}'
```

### Add a review

```bash
curl -X POST http://127.0.0.1:8000/restaurants/restaurant_12345678/reviews \
  -H "Content-Type: application/json" \
  -d '{"author":"Taylor","rating":5,"comment":"Excellent pastries."}'
```

## Data Notes

- Data is stored in memory and resets when the server stops
- IDs are generated automatically for restaurants and reviews
- Ratings must be integers from `1` to `5`
- Featured restaurants are ranked by rating, then review count, then name

## Documentation

- [Overview](docs/overview.md)
- [API Reference](docs/api.md)
- [Architecture Notes](docs/architecture.md)
