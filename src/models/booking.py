from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class Booking:
    id: str
    org_id: str
    staff_id: str
    service_id: str
    resource_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "pending"
    customer_email: str = ""
    customer_name: str = ""
    customer_phone: Optional[str] = None
    payment_id: Optional[str] = None
    payment_status: str = "unpaid"
    amount: float = 0.0
    currency: str = "USD"
    notes: Optional[str] = None
    reminders_sent: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


BOOKING_STATUS = ["pending", "confirmed", "completed", "cancelled", "no_show"]
PAYMENT_STATUS = ["unpaid", "paid", "refunded", "failed"]
