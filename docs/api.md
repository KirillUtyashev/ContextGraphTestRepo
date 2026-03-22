# API Reference

Base URL for local development:

```text
http://127.0.0.1:8000
```

All responses are JSON. The server also sends permissive CORS headers for local frontend use.

## GET /health

Returns a simple health check.

### Response

```json
{
  "status": "ok"
}
```

## GET /restaurants

Returns all restaurants, or a filtered list when query parameters are provided.

### Query Parameters

- `cuisine`: exact cuisine match, case-insensitive
- `location`: exact location match, case-insensitive
- `min_rating`: numeric minimum average rating
- `sort`: one of `name`, `rating`, or `reviews`

### Example

```bash
curl "http://127.0.0.1:8000/restaurants?location=Toronto&min_rating=4&sort=rating"
```

### Response

```json
{
  "restaurants": [
    {
      "id": "restaurant_12345678",
      "name": "Moon Noodle",
      "cuisine": "Japanese",
      "location": "Toronto",
      "price_range": "$$",
      "average_rating": 4.5,
      "review_count": 2,
      "reviews": [
        {
          "id": "review_11111111",
          "author": "Avery",
          "rating": 5,
          "comment": "Great broth and quick service."
        }
      ]
    }
  ],
  "filters": {
    "cuisine": null,
    "location": "Toronto",
    "min_rating": 4.0,
    "sort": "rating"
  },
  "count": 1
}
```

## GET /restaurants/featured

Returns featured restaurants ranked by rating, review count, and name.

### Query Parameters

- `limit`: maximum number of featured restaurants to return
- `price_range`: optional exact price range match such as `$`, `$$`, or `$$$`

### Example

```bash
curl "http://127.0.0.1:8000/restaurants/featured?limit=2&price_range=$$"
```

### Response

```json
{
  "featured": [
    {
      "id": "restaurant_87654321",
      "name": "Cedar Bistro",
      "cuisine": "French",
      "location": "Montreal",
      "price_range": "$$$",
      "average_rating": 5.0,
      "review_count": 2,
      "reviews": [
        {
          "id": "review_22222222",
          "author": "Riley",
          "rating": 5,
          "comment": "Beautiful atmosphere and standout desserts."
        }
      ],
      "feature_reason": "Top rated by the community."
    }
  ],
  "filters": {
    "price_range": "$$",
    "limit": 2
  },
  "count": 1
}
```

## GET /restaurants/<restaurant_id>

Returns a single restaurant with its reviews.

### Example

```bash
curl http://127.0.0.1:8000/restaurants/restaurant_12345678
```

## POST /restaurants

Creates a new restaurant.

### Request Body

```json
{
  "name": "Cafe Juniper",
  "cuisine": "Cafe",
  "location": "Montreal",
  "price_range": "$$"
}
```

### Response

Returns the created restaurant payload with generated `id`, `average_rating`, `review_count`, and `reviews`.

## POST /restaurants/<restaurant_id>/reviews

Creates a review for a restaurant.

### Request Body

```json
{
  "author": "Taylor",
  "rating": 5,
  "comment": "Excellent pastries."
}
```

### Response

```json
{
  "id": "review_33333333",
  "author": "Taylor",
  "rating": 5,
  "comment": "Excellent pastries."
}
```

## POST /seed

Clears the current state and loads demo restaurants and reviews.

### Response

Returns the seeded restaurant list and a `total_restaurants` count.

## POST /reset

Clears all in-memory restaurant and review data.

### Response

```json
{
  "status": "reset"
}
```

## Error Responses

Validation and lookup failures return JSON in this shape:

```json
{
  "error": "Human-readable error message."
}
```

Common cases:

- invalid rating values
- missing required request fields
- invalid query parameter types
- unknown restaurant IDs
- unknown routes
