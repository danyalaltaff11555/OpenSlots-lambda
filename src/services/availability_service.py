from datetime import datetime, timedelta
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repositories.dynamodb_repository import DynamoDBRepository


class AvailabilityService:
    def __init__(self, repo: Optional['DynamoDBRepository'] = None):
        self.repo = repo or DynamoDBRepository()

    def calculate_available_slots(
        self,
        org_id: str,
        staff_id: str,
        service_id: str,
        date: str,
        schedule: Dict,
        existing_bookings: List[Dict],
        duration: int = 60,
    ) -> List[str]:
        slots = []
        day_of_week = datetime.strptime(date, "%Y-%m-%d").weekday()
        day_schedule = schedule.get(str(day_of_week), schedule.get("default"))

        if not day_schedule:
            return slots

        start_hour, start_min = map(int, day_schedule["start"].split(":"))
        end_hour, end_min = map(int, day_schedule["end"].split(":"))

        current = datetime.strptime(f"{date} {day_schedule['start']}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{date} {day_schedule['end']}", "%Y-%m-%d %H:%M")

        booked_times = set()
        for booking in existing_bookings:
            if booking.get("staff_id") == staff_id and booking.get("status") not in [
                "cancelled",
                "no_show",
            ]:
                booked_start = datetime.fromisoformat(booking["start_time"])
                booked_end = datetime.fromisoformat(booking["end_time"])
                booked_times.add((booked_start, booked_end))

        while current + timedelta(minutes=duration) <= end:
            slot_end = current + timedelta(minutes=duration)
            is_available = True

            for booked_start, booked_end in booked_times:
                if not (current >= booked_end or slot_end <= booked_start):
                    is_available = False
                    break

            if is_available:
                slots.append(current.strftime("%H:%M"))

            current = current + timedelta(minutes=30)

        return slots

    def get_staff_schedule(self, org_id: str, staff_id: str) -> Dict:
        items = self.repo.query(f"ORG#{org_id}", f"STAFF#{staff_id}")
        for item in items:
            if item.get("entity_type") == "schedule":
                return item.get("schedule", {})
        return {}

    def get_existing_bookings(
        self, org_id: str, staff_id: str, date: str
    ) -> List[Dict]:
        date_prefix = f"BOOKING#{date}"
        bookings = self.repo.query(f"ORG#{org_id}", date_prefix)
        return [b for b in bookings if b.get("staff_id") == staff_id]
