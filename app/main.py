from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app.service import restaurant_service


def encode_json(payload: object) -> bytes:
    return json.dumps(payload).encode("utf-8")


def parse_json_body(body: bytes) -> dict:
    if not body:
        return {}

    return json.loads(body.decode("utf-8"))


class RestaurantHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_common_headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        parts = self._path_parts(path)
        query = parse_qs(parsed_url.query)

        try:
            if path == "/health":
                self._send_json(HTTPStatus.OK, {"status": "ok"})
                return

            if path == "/restaurants":
                min_rating = self._read_float(query, "min_rating")
                restaurants = restaurant_service.search_restaurants(
                    cuisine=self._read_query_value(query, "cuisine"),
                    location=self._read_query_value(query, "location"),
                    min_rating=min_rating,
                    sort=self._read_query_value(query, "sort") or "name",
                )
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "restaurants": restaurants,
                        "filters": {
                            "cuisine": self._read_query_value(query, "cuisine"),
                            "location": self._read_query_value(query, "location"),
                            "min_rating": min_rating,
                            "sort": self._read_query_value(query, "sort") or "name",
                        },
                        "count": len(restaurants),
                    },
                )
                return

            if path == "/restaurants/featured":
                limit = self._read_int(query, "limit") or 3
                featured = restaurant_service.get_featured_restaurants(limit=limit)
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "featured": featured,
                        "count": len(featured),
                    },
                )
                return

            if len(parts) == 2 and parts[0] == "restaurants":
                self._send_json(HTTPStatus.OK, restaurant_service.get_restaurant(parts[1]))
                return

            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})
        except ValueError as exc:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": str(exc)})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        parts = self._path_parts(path)

        try:
            payload = self._read_request_json()

            if path == "/restaurants":
                restaurant = restaurant_service.create_restaurant(
                    name=payload.get("name", ""),
                    cuisine=payload.get("cuisine", ""),
                    location=payload.get("location", ""),
                    price_range=payload.get("price_range", ""),
                    restaurant_id=payload.get("id"),
                )
                self._send_json(HTTPStatus.CREATED, restaurant)
                return

            if len(parts) == 3 and parts[0] == "restaurants" and parts[2] == "reviews":
                review = restaurant_service.add_review(
                    restaurant_id=parts[1],
                    author=payload.get("author", ""),
                    rating=int(payload.get("rating", 0)),
                    comment=payload.get("comment", ""),
                    review_id=payload.get("id"),
                )
                self._send_json(HTTPStatus.CREATED, review)
                return

            if path == "/seed":
                self._send_json(HTTPStatus.CREATED, restaurant_service.seed_demo_data())
                return

            if path == "/reset":
                restaurant_service.reset()
                self._send_json(HTTPStatus.OK, {"status": "reset"})
                return

            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception as exc:  # pragma: no cover - defensive path
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_request_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        return parse_json_body(body)

    def _send_json(self, status: HTTPStatus, payload: dict) -> None:
        response = encode_json(payload)
        self.send_response(status)
        self._send_common_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def _send_common_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    @staticmethod
    def _path_parts(path: str) -> list[str]:
        return [part for part in path.strip("/").split("/") if part]

    @staticmethod
    def _read_query_value(query: dict[str, list[str]], key: str) -> str | None:
        values = query.get(key)
        if not values:
            return None
        return values[0].strip() or None

    @staticmethod
    def _read_float(query: dict[str, list[str]], key: str) -> float | None:
        value = RestaurantHandler._read_query_value(query, key)
        if value is None:
            return None

        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"Query parameter '{key}' must be a number.") from exc

    @staticmethod
    def _read_int(query: dict[str, list[str]], key: str) -> int | None:
        value = RestaurantHandler._read_query_value(query, key)
        if value is None:
            return None

        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"Query parameter '{key}' must be an integer.") from exc


def run() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    server = ThreadingHTTPServer((host, port), RestaurantHandler)
    print(f"Restaurant review backend running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
