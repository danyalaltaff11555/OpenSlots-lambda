from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4
import stripe
import config
from repositories.dynamodb_repository import DynamoDBRepository


class PaymentService:
    def __init__(self, repo: Optional[DynamoDBRepository] = None):
        self.repo = repo or DynamoDBRepository()
        stripe.api_key = config.STRIPE_SECRET_KEY

    def create_payment_intent(
        self, booking_id: str, org_id: str, amount: int, currency: str = "usd"
    ) -> Dict:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency,
            metadata={"booking_id": booking_id, "org_id": org_id},
        )

        payment = {
            "PK": f"ORG#{org_id}",
            "SK": f"PAYMENT#{booking_id}",
            "id": str(uuid4())[:8],
            "booking_id": booking_id,
            "org_id": org_id,
            "entity_type": "payment",
            "stripe_payment_intent_id": intent.id,
            "amount": amount,
            "currency": currency,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        self.repo.put_item(payment)
        return {"client_secret": intent.client_secret, "payment_id": payment["id"]}

    def confirm_payment(self, booking_id: str, org_id: str) -> Dict:
        payment = self.repo.get_item(f"ORG#{org_id}", f"PAYMENT#{booking_id}")
        if not payment:
            raise Exception("Payment not found")

        intent = stripe.PaymentIntent.retrieve(payment["stripe_payment_intent_id"])

        status = "succeeded" if intent.status == "succeeded" else "failed"

        updated = {
            "status": status,
            "stripe_charge_id": intent.latest_charge,
            "updated_at": datetime.utcnow().isoformat(),
        }

        self.repo.update_item(f"ORG#{org_id}", f"PAYMENT#{booking_id}", updated)
        return {**payment, **updated}

    def process_refund(
        self, booking_id: str, org_id: str, amount: Optional[float] = None
    ) -> Dict:
        payment = self.repo.get_item(f"ORG#{org_id}", f"PAYMENT#{booking_id}")
        if not payment:
            raise Exception("Payment not found")

        refund_amount = amount or payment["amount"]
        refund = stripe.Refund.create(
            payment_intent=payment["stripe_payment_intent_id"],
            amount=int(refund_amount * 100) if refund_amount else None,
        )

        refund_record = {
            "PK": f"ORG#{org_id}",
            "SK": f"REFUND#{payment['id']}",
            "id": refund.id,
            "booking_id": booking_id,
            "payment_id": payment["id"],
            "org_id": org_id,
            "amount": refund_amount,
            "status": "succeeded",
            "created_at": datetime.utcnow().isoformat(),
        }

        self.repo.put_item(refund_record)

        updated_payment = {
            "status": "refunded" if refund_amount == payment["amount"] else "partially_refunded",
            "refund_id": refund.id,
            "refund_amount": refund_amount,
            "updated_at": datetime.utcnow().isoformat(),
        }

        self.repo.update_item(f"ORG#{org_id}", f"PAYMENT#{booking_id}", updated_payment)
        return {**payment, **updated_payment}
