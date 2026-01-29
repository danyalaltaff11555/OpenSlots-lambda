import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import uuid4
from utils.response import success_response, error_response
from utils.auth import validate_token, extract_token
from utils.logging import log_event
from repositories.dynamodb_repository import DynamoDBRepository


class BookingHandler:
    def __init__(self, repo: Optional[DynamoDBRepository] = None):
        self.repo = repo or DynamoDBRepository()

    def _pk(self, org_id: str) -> str:
        return f"ORG#{org_id}"

    def _sk(self, booking_id: str) -> str:
        return f"BOOKING#{booking_id}"

    def create(self, org_id: str, data: Dict) -> Dict:
        booking_id = str(uuid4())[:8]
        start = datetime.fromisoformat(data["start_time"])
        end = start + timedelta(minutes=data.get("duration", 60))

        booking = {
            "PK": self._pk(org_id),
            "SK": self._sk(booking_id),
            "id": booking_id,
            "org_id": org_id,
            "entity_type": "booking",
            "staff_id": data["staff_id"],
            "service_id": data["service_id"],
            "resource_id": data.get("resource_id"),
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
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

        if not self.repo.atomic_put(booking):
            raise Exception("Slot already booked")

        return booking

    def get(self, org_id: str, booking_id: str) -> Optional[Dict]:
        return self.repo.get_item(self._pk(org_id), self._sk(booking_id))

    def update(self, org_id: str, booking_id: str, data: Dict) -> Optional[Dict]:
        updates = {**data, "updated_at": datetime.utcnow().isoformat()}
        self.repo.update_item(self._pk(org_id), self._sk(booking_id), updates)
        return self.get(org_id, booking_id)

    def delete(self, org_id: str, booking_id: str) -> bool:
        booking = self.get(org_id, booking_id)
        if not booking:
            return False
        self.repo.delete_item(self._pk(org_id), self._sk(booking_id))
        return True

    def list(self, org_id: str, params: Dict) -> list:
        bookings = self.repo.query(self._pk(org_id), "BOOKING#")
        if staff_id := params.get("staff_id"):
            bookings = [b for b in bookings if b.get("staff_id") == staff_id]
        if status := params.get("status"):
            bookings = [b for b in bookings if b.get("status") == status]
        if date := params.get("date"):
            bookings = [b for b in bookings if b.get("start_time", "").startswith(date)]
        return bookings


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = json.loads(event.get("body", "{}"))
        auth_header = event.get("headers", {}).get("Authorization", "")
        token = extract_token(auth_header)
        payload = validate_token(token)
        org_id = payload.org_id

        handler = BookingHandler()
        method = event.get("httpMethod", "")
        path = event.get("path", "")
        path_params = event.get("pathParameters", {}) or {}

        if method == "POST" and "/bookings" in path:
            booking = handler.create(org_id, body)
            log_event("booking_created", {"id": booking["id"], "org_id": org_id})
            return success_response(booking, status_code=201)

        if method == "GET" and "/bookings" in path:
            if booking_id := path_params.get("id"):
                booking = handler.get(org_id, booking_id)
                if not booking:
                    return error_response("Booking not found", status_code=404)
                return success_response(booking)
            params = event.get("queryStringParameters", {}) or {}
            return success_response(handler.list(org_id, params))

        if method == "PATCH" and (booking_id := path_params.get("id")):
            booking = handler.update(org_id, booking_id, body)
            return success_response(booking)

        if method == "DELETE" and (booking_id := path_params.get("id")):
            if handler.delete(org_id, booking_id):
                log_event("booking_cancelled", {"id": booking_id, "org_id": org_id})
                return success_response({"deleted": True})
            return error_response("Booking not found", status_code=404)

        return error_response("Method not allowed", status_code=405)

    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(str(e), status_code=400)
