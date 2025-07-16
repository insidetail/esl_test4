from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from stripe_webhook import stripe_webhook
from authen import sign_up, login, get_current_user
import stripe
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.post("/signup")
def signup_api(request: Request):
    return sign_up(request)

@app.post("/login")
def login_api(request: Request):
    return login(request)

# @app.post("/create-checkout-session")
# async def create_checkout_session(request: Request, user=Depends(get_current_user)):
#     email = user['email']
#     user_id = user['id']
#
#     customer = stripe.Customer.create(
#         email=email,
#         metadata={"user_id": user_id}
#     )
#
#     session = stripe.checkout.Session.create(
#         customer=customer.id,
#         payment_method_types=["card"],
#         mode="subscription",
#         line_items=[{
#             "price": os.getenv("STRIPE_PRICE_ID"),
#             "quantity": 1,
#         }],
#         success_url=os.getenv("SUCCESS_URL"),
#         cancel_url=os.getenv("CANCEL_URL"),
#     )
#
#     return {"url": session.url}
#
# app.post("/stripe-webhook")(stripe_webhook)