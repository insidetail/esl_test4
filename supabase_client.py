import os
import requests
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}


def get_all_products(table_name: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def insert_product(data: dict, table_name: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    headers = HEADERS.copy()
    headers["Prefer"] = "return=representation"
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def update_product_by_name(name: str, updates: dict, table_name: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?name=eq.{name}"
    headers = HEADERS.copy()
    headers["Prefer"] = "return=representation"
    response = requests.patch(url, headers=headers, json=updates)
    response.raise_for_status()
    return response.json()


def delete_product_by_name(name: str, table_name: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?name=eq.{name}"
    response = requests.delete(url, headers=HEADERS)
    response.raise_for_status()
    return response.status_code == 204