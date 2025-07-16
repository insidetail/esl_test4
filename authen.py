from fastapi import Request, HTTPException, Header
import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def sign_up(request: Request):
    body = request.json()
    email = body['email']
    password = body['password']

    res = requests.post(f"{SUPABASE_URL}/auth/v1/signup", json={
        "email": email,
        "password": password
    }, headers={"apikey": SUPABASE_ANON_KEY, "Content-Type": "application/json"})

    if res.status_code == 200:
        user_id = res.json()['user']['id']
        requests.post(f"{SUPABASE_URL}/rest/v1/users", json={
            "id": user_id,
            "email": email,
            "subscription_status": "free",
            "plan": "free"
        }, headers={"apikey": SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {res.json()['access_token']}",
                    "Content-Type": "application/json"})

    return res.json()

def login(request: Request):
    body = request.json()
    email = body['email']
    password = body['password']

    res = requests.post(f"{SUPABASE_URL}/auth/v1/token?grant_type=password", json={
        "email": email,
        "password": password
    }, headers={"apikey": SUPABASE_ANON_KEY, "Content-Type": "application/json"})

    return res.json()

def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    res = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers={
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {token}"
    })
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return res.json()