from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import uuid4
from repositories.dynamodb_repository import DynamoDBRepository


class BookingService:
    def __init__(self, repo: Optional[DynamoDBRepository] = None):
        self.repo = repo or DynamoDBRepository()

    def create_booking(self, org_id: str, data: Dict) -> Dict:
        booking_id = str(uuid4())[:8]
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = start_time + timedelta(minutes=data.get("duration", 60))

        booking = {
            "PK": f"ORG#{org_id}",
            "SK": f"BOOKING#{booking_id}",
            "id": booking_id,
            "org_id": org_id,
            "entity_type": "booking",
            "staff_id": data["staff_id"],
            "service_id": data["service_id"],
            "resource_id": data.get("resource_id"),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "status": "pending",
            "customer_email": data["customer_email"],
            "customer_name": data["customer_name"],
            "customer_phone": data.get("customer_phone"),
            "payment_status": "unpaid",
            "amount": data.get("amount", 0),
            "currency": data.get("currency", "USD"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        success = self.repo.atomic_put(booking)

        if not success:
            raise Exception("Slot already booked")

        return booking

    def get_booking(self, org_id: str, booking_id: str) -> Optional[Dict]:
        return self.repo.get_item(f"ORG#{org_id}", f"BOOKING#{booking_id}")

    def list_bookings(
        self,
        org_id: str,
        staff_id: Optional[str] = None,
        status: Optional[str] = None,
        date: Optional[str] = None,
    ) -> List[Dict]:
        bookings = self.repo.query(f"ORG#{org_id}", "BOOKING#")

        if staff_id:
            bookings = [b for b in bookings if b.get("staff_id") == staff_id]
        if status:
            bookings = [b for b in bookings if b.get("status") == status]
        if date:
            bookings = [b for b in bookings if b.get("start_time", "").startswith(date)]

        return bookings

    def update_booking(self, org_id: str, booking_id: str, updates: Dict) -> Optional[Dict]:
        update_data = {**updates, "updated_at": datetime.utcnow().isoformat()}
        self.repo.update_item(
            f"ORG#{org_id}", f"BOOKING#{booking_id}", update_data
        )
        return self.get_booking(org_id, booking_id)

    def cancel_booking(self, org_id: str, booking_id: str) -> Optional[Dict]:
        return self.update_booking(org_id, booking_id, {"status": "cancelled"})

    def confirm_booking(self, org_id: str, booking_id: str) -> Optional[Dict]:
        return self.update_booking(org_id, booking_id, {"status": "confirmed"})

    def reschedule_booking(
        self, org_id: str, booking_id: str, new_start_time: str
    ) -> Optional[Dict]:
        old_booking = self.get_booking(org_id, booking_id)
        if not old_booking:
            raise Exception("Booking not found")

        duration = int(
            (
                datetime.fromisoformat(old_booking["end_time"])
                - datetime.fromisoformat(old_booking["start_time"])
            ).total_seconds()
            / 60
        )

        new_start = datetime.fromisoformat(new_start_time)
        new_end = new_start + timedelta(minutes=duration)

        return self.update_booking(org_id, booking_id, {
            "start_time": new_start.isoformat(),
            "end_time": new_end.isoformat(),
        })
