import pytest
from datetime import datetime, timedelta
from services.booking_service import BookingService


def test_create_booking_success():
    service = BookingService()
    data = {
        "staff_id": "staff1",
        "service_id": "service1",
        "start_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "customer_email": "test@example.com",
        "customer_name": "Test User",
        "duration": 60,
    }

    booking = service.create_booking("org1", data)

    assert booking["org_id"] == "org1"
    assert booking["staff_id"] == "staff1"
    assert booking["status"] == "pending"
    assert "id" in booking


def test_get_booking_not_found():
    service = BookingService()
    booking = service.get_booking("org1", "nonexistent")

    assert booking is None


def test_cancel_booking():
    service = BookingService()
    data = {
        "staff_id": "staff1",
        "service_id": "service1",
        "start_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "customer_email": "test@example.com",
        "customer_name": "Test User",
        "duration": 60,
    }

    booking = service.create_booking("org1", data)
    cancelled = service.cancel_booking("org1", booking["id"])

    assert cancelled["status"] == "cancelled"
