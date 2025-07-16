from fastapi import Request
import stripe
import os
from supabase_client import supabase
import json

async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return {"error": str(e)}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]
        user_id = session["metadata"]["user_id"]

        supabase.table("users").update({
            "stripe_customer_id": customer_id,
            "subscription_status": "active",
            "plan": "basic"
        }).eq("id", user_id).execute()

    return {"status": "success"}