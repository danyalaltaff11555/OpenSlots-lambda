from datetime import datetime, timedelta
from typing import Dict, Optional
from repositories.dynamodb_repository import DynamoDBRepository


class CancellationService:
    def __init__(self, repo: Optional[DynamoDBRepository] = None):
        self.repo = repo or DynamoDBRepository()

    def calculate_refund(
        self,
        booking: Dict,
        cancellation_time: datetime,
        policy: Optional[Dict] = None,
    ) -> Dict:
        if not policy:
            policy = {
                "full_refund_hours": 24,
                "partial_refund_percent": 50,
                "no_refund_hours": 2,
            }

        start_time = datetime.fromisoformat(booking["start_time"])
        hours_until_booking = (start_time - cancellation_time).total_seconds() / 3600

        if hours_until_booking >= policy.get("full_refund_hours", 24):
            return {
                "refund_amount": booking["amount"],
                "refund_percent": 100,
                "reason": "Full refund - cancelled within policy window",
            }

        elif hours_until_booking >= policy.get("no_refund_hours", 2):
            partial_percent = policy.get("partial_refund_percent", 50)
            return {
                "refund_amount": booking["amount"] * (partial_percent / 100),
                "refund_percent": partial_percent,
                "reason": f"Partial refund - {partial_percent}% within policy window",
            }

        else:
            return {
                "refund_amount": 0,
                "refund_percent": 0,
                "reason": "No refund - cancelled within no-refund window",
            }

    def process_cancellation(self, org_id: str, booking_id: str) -> Dict:
        booking = self.repo.get_item(f"ORG#{org_id}", f"BOOKING#{booking_id}")
        if not booking:
            raise Exception("Booking not found")

        if booking["status"] == "cancelled":
            raise Exception("Booking already cancelled")

        cancellation_time = datetime.utcnow()
        refund_info = self.calculate_refund(booking, cancellation_time)

        updates = {
            "status": "cancelled",
            "cancellation_time": cancellation_time.isoformat(),
            "refund_amount": refund_info["refund_amount"],
            "refund_percent": refund_info["refund_percent"],
            "cancellation_reason": refund_info["reason"],
            "updated_at": cancellation_time.isoformat(),
        }

        self.repo.update_item(f"ORG#{org_id}", f"BOOKING#{booking_id}", updates)
        return {**booking, **updates}

    def apply_no_show_policy(
        self, org_id: str, booking_id: str, policy: Dict
    ) -> Dict:
        booking = self.repo.get_item(f"ORG#{org_id}", f"BOOKING#{booking_id}")
        if not booking:
            raise Exception("Booking not found")

        no_show_fee = policy.get("no_show_fee", 0)
        updates = {
            "status": "no_show",
            "no_show_fee": no_show_fee,
            "updated_at": datetime.utcnow().isoformat(),
        }

        self.repo.update_item(f"ORG#{org_id}", f"BOOKING#{booking_id}", updates)
        return {**booking, **updates}
