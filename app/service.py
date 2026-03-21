from __future__ import annotations

from dataclasses import asdict, dataclass, field
from threading import Lock
from typing import Any

from app.recommendations import rank_featured_restaurants
from app.utils import make_id


@dataclass
class Review:
    id: str
    author: str
    rating: int
    comment: str


@dataclass
class Restaurant:
    id: str
    name: str
    cuisine: str
    location: str
    price_range: str
    reviews: list[Review] = field(default_factory=list)


class RestaurantService:
    def __init__(self) -> None:
        self._lock = Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._restaurants: dict[str, Restaurant] = {}

    def create_restaurant(
        self,
        name: str,
        cuisine: str,
        location: str,
        price_range: str,
        restaurant_id: str | None = None,
    ) -> dict[str, Any]:
        if not all([name, cuisine, location, price_range]):
            raise ValueError("Name, cuisine, location, and price_range are required.")

        restaurant = Restaurant(
            id=restaurant_id or make_id("restaurant"),
            name=name,
            cuisine=cuisine,
            location=location,
            price_range=price_range,
        )

        with self._lock:
            if restaurant.id in self._restaurants:
                raise ValueError(f"Restaurant '{restaurant.id}' already exists.")
            self._restaurants[restaurant.id] = restaurant

        return self.build_restaurant_payload(restaurant)

    def list_restaurants(self) -> list[dict[str, Any]]:
        with self._lock:
            return [self.build_restaurant_payload(restaurant) for restaurant in self._restaurants.values()]

    def search_restaurants(
        self,
        cuisine: str | None = None,
        location: str | None = None,
        min_rating: float | None = None,
        sort: str = "name",
    ) -> list[dict[str, Any]]:
        restaurants = self.list_restaurants()

        if cuisine:
            normalized_cuisine = cuisine.strip().lower()
            restaurants = [
                restaurant for restaurant in restaurants
                if restaurant["cuisine"].lower() == normalized_cuisine
            ]

        if location:
            normalized_location = location.strip().lower()
            restaurants = [
                restaurant for restaurant in restaurants
                if restaurant["location"].lower() == normalized_location
            ]

        if min_rating is not None:
            restaurants = [
                restaurant for restaurant in restaurants
                if restaurant["average_rating"] is not None and restaurant["average_rating"] >= min_rating
            ]

        if sort == "rating":
            restaurants.sort(
                key=lambda restaurant: (
                    restaurant["average_rating"] is None,
                    -(restaurant["average_rating"] or 0),
                    restaurant["name"].lower(),
                )
            )
        elif sort == "reviews":
            restaurants.sort(
                key=lambda restaurant: (-restaurant["review_count"], restaurant["name"].lower())
            )
        else:
            restaurants.sort(key=lambda restaurant: restaurant["name"].lower())

        return restaurants

    def get_restaurant(self, restaurant_id: str) -> dict[str, Any]:
        with self._lock:
            restaurant = self._restaurants.get(restaurant_id)
            if restaurant is None:
                raise ValueError(f"Restaurant '{restaurant_id}' was not found.")
            return self.build_restaurant_payload(restaurant)

    def get_featured_restaurants(self, limit: int = 3) -> list[dict[str, Any]]:
        if limit < 1:
            raise ValueError("limit must be at least 1.")

        restaurants = self.list_restaurants()
        return rank_featured_restaurants(restaurants, limit=limit)

    def add_review(
        self,
        restaurant_id: str,
        author: str,
        rating: int,
        comment: str,
        review_id: str | None = None,
    ) -> dict[str, Any]:
        if not restaurant_id:
            raise ValueError("restaurant_id is required.")
        if not author or not comment:
            raise ValueError("Author and comment are required.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        with self._lock:
            restaurant = self._restaurants.get(restaurant_id)
            if restaurant is None:
                raise ValueError(f"Restaurant '{restaurant_id}' was not found.")

            review = Review(
                id=review_id or make_id("review"),
                author=author,
                rating=rating,
                comment=comment,
            )
            restaurant.reviews.append(review)

        return self.serialize_review(review)

    def seed_demo_data(self) -> dict[str, Any]:
        self.reset()
        noodle_shop = self.create_restaurant("Moon Noodle", "Japanese", "Toronto", "$$")
        diner = self.create_restaurant("Parkside Diner", "Comfort Food", "Ottawa", "$")
        bistro = self.create_restaurant("Cedar Bistro", "French", "Montreal", "$$$")
        self.add_review(noodle_shop["id"], "Avery", 5, "Great broth and quick service.")
        self.add_review(noodle_shop["id"], "Jordan", 4, "Solid ramen for a casual dinner.")
        self.add_review(diner["id"], "Sam", 4, "Excellent brunch and friendly staff.")
        self.add_review(bistro["id"], "Riley", 5, "Beautiful atmosphere and standout desserts.")
        self.add_review(bistro["id"], "Morgan", 5, "Perfect date-night spot.")
        return {
            "restaurants": self.list_restaurants(),
            "total_restaurants": len(self._restaurants),
        }

    @staticmethod
    def serialize_review(review: Review) -> dict[str, Any]:
        return asdict(review)

    def build_restaurant_payload(self, restaurant: Restaurant) -> dict[str, Any]:
        review_count = len(restaurant.reviews)
        average_rating = round(
            sum(review.rating for review in restaurant.reviews) / review_count,
            1,
        ) if review_count else None

        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "cuisine": restaurant.cuisine,
            "location": restaurant.location,
            "price_range": restaurant.price_range,
            "average_rating": average_rating,
            "review_count": review_count,
            "reviews": [self.serialize_review(review) for review in restaurant.reviews],
        }


restaurant_service = RestaurantService()
