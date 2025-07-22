import os
import requests
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def build_headers(jwt_token: str):
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }


def get_all_products(table_name: str, jwt_token: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    headers = build_headers(jwt_token)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def insert_product(data: dict, table_name: str, jwt_token: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    headers = build_headers(jwt_token)
    headers["Prefer"] = "return=representation"
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def update_product_by_name(name: str, updates: dict, table_name: str, jwt_token: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?name=eq.{name}"
    headers = build_headers(jwt_token)
    headers["Prefer"] = "return=representation"
    response = requests.patch(url, headers=headers, json=updates)
    response.raise_for_status()
    return response.json()


def delete_product_by_name(name: str, table_name: str, jwt_token: str):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?name=eq.{name}"
    headers = build_headers(jwt_token)
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code == 204