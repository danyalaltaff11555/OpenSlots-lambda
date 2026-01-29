import pytest
from datetime import datetime, timedelta
from services.cancellation_service import CancellationService


def test_full_refund_calculation():
    service = CancellationService()
    booking = {
        "amount": 100,
        "start_time": (datetime.utcnow() + timedelta(days=2)).isoformat(),
    }

    result = service.calculate_refund(booking, datetime.utcnow())

    assert result["refund_amount"] == 100
    assert result["refund_percent"] == 100


def test_partial_refund_calculation():
    service = CancellationService()
    booking = {
        "amount": 100,
        "start_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
    }

    result = service.calculate_refund(booking, datetime.utcnow())

    assert result["refund_amount"] == 50
    assert result["refund_percent"] == 50


def test_no_refund_calculation():
    service = CancellationService()
    booking = {
        "amount": 100,
        "start_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }

    result = service.calculate_refund(booking, datetime.utcnow())

    assert result["refund_amount"] == 0
    assert result["refund_percent"] == 0
