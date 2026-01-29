import json
from typing import Any, Dict
from utils.response import success_response, error_response
from utils.auth import validate_token, extract_token
from services.payment_service import PaymentService


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = json.loads(event.get("body", "{}"))
        auth_header = event.get("headers", {}).get("Authorization", "")
        token = extract_token(auth_header)
        payload = validate_token(token)
        org_id = payload.org_id

        if event.get("httpMethod") == "POST" and "/payments" in event.get("path", ""):
            service = PaymentService()
            booking_id = body.get("booking_id")
            amount = body.get("amount")

            if not booking_id or not amount:
                return error_response("booking_id and amount required", status_code=400)

            result = service.create_payment_intent(booking_id, org_id, amount)
            return success_response(result, status_code=201)

        return error_response("Method not allowed", status_code=405)

    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(str(e), status_code=400)


def webhook_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        import stripe
        import config

        payload = json.loads(event.get("body", ""))
        sig = event.get("headers", {}).get("Stripe-Signature", "")

        stripe.Event.construct_from(payload, config.STRIPE_WEBHOOK_SECRET, sig)

        event_type = payload.get("type")
        if event_type == "payment_intent.succeeded":
            metadata = payload.get("data", {}).get("object", {}).get("metadata", {})
            booking_id = metadata.get("booking_id")
            if booking_id:
                service = PaymentService()
                service.confirm_payment(booking_id, metadata.get("org_id", ""))

        return success_response({"received": True})

    except Exception as e:
        print(f"Webhook Error: {str(e)}")
        return error_response(str(e), status_code=400)
