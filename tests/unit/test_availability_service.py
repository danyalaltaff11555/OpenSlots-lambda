import pytest
from datetime import datetime, timedelta
from services.availability_service import AvailabilityService


def test_calculate_slots_no_bookings():
    schedule = {"0": {"start": "09:00", "end": "17:00"}}
    existing = []
    date = datetime.utcnow().strftime("%Y-%m-%d")

    service = AvailabilityService()
    slots = service.calculate_available_slots(
        "org1", "staff1", "service1", date, schedule, existing, 60
    )

    assert len(slots) == 8
    assert "09:00" in slots


def test_calculate_slots_with_bookings():
    schedule = {"0": {"start": "09:00", "end": "12:00"}}
    now = datetime.utcnow()
    date = now.strftime("%Y-%m-%d")

    existing = [
        {
            "staff_id": "staff1",
            "status": "confirmed",
            "start_time": (now + timedelta(hours=1)).isoformat(),
            "end_time": (now + timedelta(hours=2)).isoformat(),
        }
    ]

    service = AvailabilityService()
    slots = service.calculate_available_slots(
        "org1", "staff1", "service1", date, schedule, existing, 60
    )

    assert "09:00" in slots
    assert "10:00" not in slots


def test_calculate_slots_outside_business_hours():
    schedule = {"0": {"start": "09:00", "end": "10:00"}}
    date = datetime.utcnow().strftime("%Y-%m-%d")
    existing = []

    service = AvailabilityService()
    slots = service.calculate_available_slots(
        "org1", "staff1", "service1", date, schedule, existing, 60
    )

    assert len(slots) == 1
    assert "09:00" in slots
