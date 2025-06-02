import json
import re
from config import ROUTES_JSON_PATH
from src.city_aliases import normalize_city, all_city_aliases

with open(ROUTES_JSON_PATH, encoding="utf-8") as f:
    ROUTES = json.load(f)

def find_route(start, end):
    start = normalize_city(start)
    end = normalize_city(end)

    for route in ROUTES:
        all_points = [route["start"].lower()] + [stop["city"].lower() for stop in route.get("stops", [])] + [route["end"].lower()]
        if start in all_points and end in all_points:
            if all_points.index(start) < all_points.index(end):  # ensure direction
                return route
    return None

def extract_cities_from_text(text: str):
    text = text.lower()
    found = []
    for alias, city in all_city_aliases.items():
        if alias in text and city not in found:
            found.append(city)
    return found
