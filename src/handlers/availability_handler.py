import json
from typing import Any, Dict
from utils.response import success_response, error_response
from utils.auth import validate_token, extract_token
from services.availability_service import AvailabilityService


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        auth_header = event.get("headers", {}).get("Authorization", "")
        token = extract_token(auth_header)
        payload = validate_token(token)
        org_id = payload.org_id

        params = event.get("queryStringParameters", {}) or {}
        service_id = params.get("service_id")
        staff_id = params.get("staff_id")
        date = params.get("date")
        duration = int(params.get("duration", 60))

        if not all([service_id, date]):
            return error_response("service_id and date are required", status_code=400)

        service = AvailabilityService()
        schedule = service.get_staff_schedule(org_id, staff_id or "")
        bookings = service.get_existing_bookings(org_id, staff_id or "", date)

        slots = service.calculate_available_slots(
            org_id,
            staff_id or "",
            service_id,
            date,
            schedule,
            bookings,
            duration,
        )

        return success_response({"date": date, "available_slots": slots})

    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(str(e), status_code=400)
