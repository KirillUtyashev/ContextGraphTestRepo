from __future__ import annotations

from typing import Any


def rank_featured_restaurants(
    restaurants: list[dict[str, Any]],
    limit: int = 3,
) -> list[dict[str, Any]]:
    ranked = sorted(
        restaurants,
        key=lambda restaurant: (
            -(restaurant["average_rating"] or 0),
            -restaurant["review_count"],
            restaurant["name"].lower(),
        ),
    )

    featured: list[dict[str, Any]] = []
    for restaurant in ranked[:limit]:
        featured.append(
            {
                **restaurant,
                "feature_reason": build_feature_reason(restaurant),
            }
        )

    return featured


def build_feature_reason(restaurant: dict[str, Any]) -> str:
    rating = restaurant["average_rating"]
    review_count = restaurant["review_count"]

    if rating is None or review_count == 0:
        return "New listing worth checking out."

    if rating >= 4.5 and review_count >= 2:
        return "Top rated by the community."

    if review_count >= 3:
        return "Popular with a steady stream of reviews."

    return "Highly rated and trending."
