# Architecture Notes

This backend is intentionally simple. It uses a small set of modules with clear responsibilities so the app is easy to understand and extend.

## Module Responsibilities

### `app/main.py`

This is the HTTP entrypoint. It:

- starts the `ThreadingHTTPServer`
- defines the request handler
- parses route paths and query parameters
- reads JSON request bodies
- writes JSON responses
- maps incoming requests to service-layer methods

### `app/service.py`

This is the core application layer. It:

- defines the `Restaurant` and `Review` data models
- stores in-memory restaurant state
- validates input data
- creates restaurants and reviews
- searches and filters restaurant data
- builds API payloads for responses
- seeds demo data

### `app/recommendations.py`

This module contains recommendation logic. It:

- ranks restaurants for the featured endpoint
- explains why a restaurant was featured

Keeping this logic separate makes it easier to swap in more advanced ranking rules later.

## Request Flow

Typical request flow:

1. A request hits `RestaurantHandler` in `app/main.py`
2. The handler parses the route and request data
3. The handler calls a method on `restaurant_service`
4. The service validates and processes the request
5. The handler returns a JSON response

For featured recommendations, the flow adds one extra step:

1. `app/main.py` calls `restaurant_service.get_featured_restaurants()`
2. `app/service.py` gathers restaurant payloads
3. `app/recommendations.py` ranks and annotates them
4. `app/main.py` returns the final JSON response

## Data Storage

The app uses in-memory storage only:

- restaurants are stored in a dictionary keyed by restaurant ID
- reviews are stored inside each restaurant object
- no data is persisted to disk

This makes the app easy to reset and ideal for demo repos, but it also means:

- server restarts erase data
- the app is not suitable for production use as-is

## Concurrency

The service uses a `Lock` around shared in-memory state. That is enough for this small threaded server and helps avoid inconsistent writes when multiple requests arrive at the same time.

## Extension Ideas

Natural next steps for this codebase would be:

- add pagination for large restaurant lists
- add update and delete endpoints
- add restaurant tags or categories
- persist data with SQLite or Postgres
- move the API to FastAPI or Flask
- add automated tests
