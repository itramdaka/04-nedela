import json
import os

SHOPPING_FILE = "shopping.json"
PRICES_FILE = "prices.json"

# --- Iepirkumu saraksta operācijas ---
def load_list():
    """Nolasa shopping.json. Ja neeksistē, atgriež []"""
    if not os.path.exists(SHOPPING_FILE):
        return []
    with open(SHOPPING_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_list(items):
    """Saglabā iepirkumu sarakstu shopping.json"""
    with open(SHOPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

# --- Cenu datubāzes operācijas (3. solis) ---
def load_prices():
    """Nolasa prices.json. Ja neeksistē, atgriež {}"""
    if not os.path.exists(PRICES_FILE):
        return {}
    with open(PRICES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_prices(prices):
    """Saglabā cenu vārdnīcu prices.json"""
    with open(PRICES_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=2, ensure_ascii=False)

def get_price(name):
    """Atgriež cenu no DB vai None"""
    prices = load_prices()
    return prices.get(name)

def set_price(name, price):
    """Saglabā vai atjaunina cenu datubāzē"""
    prices = load_prices()
    prices[name] = price
    save_prices(prices)