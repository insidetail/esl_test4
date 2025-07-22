from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.templating import Jinja2Templates

from stripe_webhook import stripe_webhook
from authen import sign_up, login, get_current_user
import supabase_client
import stripe
import os
import json

from dotenv import load_dotenv      # デバッグ
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.post("/signup")
async def signup_api(request: Request):
    return await sign_up(request)

@app.post("/login")
async def login_api(request: Request):
    return await login(request)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("first_login.html", {"request": request})

# アカウント登録画面の表示
@app.get("/account_touroku", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("account_touroku.html", {"request": request})

# メインメニューの表示
@app.get("/show_main_menu", response_class=HTMLResponse)
async def menu_page(request: Request):
    return templates.TemplateResponse("main_menu.html", {"request": request})

# 商品一覧(ユーザーIDで抽出したもの)を取得
@app.get("/get_users_products")
def get_users_products(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    products = supabase_client.get_all_products("products_and_user_ids", token)
    print(f"products: {products}")
    return {"products": products}

# 商品一覧(ユーザーIDで抽出したもの)を表示
@app.get("/products_show", response_class=HTMLResponse)
async def products_show(request: Request):
    return templates.TemplateResponse("shouhin_ichiran.html", {"request": request})

# 支払？
@app.post("/create-checkout-session")
async def create_checkout_session(request: Request, user=Depends(get_current_user)):
    email = user['email']
    user_id = user['id']

    customer = stripe.Customer.create(
        email=email,
        metadata={"user_id": user_id}
    )

    session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1,
        }],
        success_url=os.getenv("SUCCESS_URL"),
        cancel_url=os.getenv("CANCEL_URL"),
    )

    return {"url": session.url}

    app.post("/stripe-webhook")(stripe_webhook)

# デバッグ
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)