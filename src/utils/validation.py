from pydantic import BaseModel
from typing import Optional


class BookingRequest(BaseModel):
    org_id: str
    staff_id: str
    service_id: str
    resource_id: Optional[str] = None
    start_time: str
    customer_email: str
    customer_name: str
    customer_phone: Optional[str] = None


class AvailabilityQuery(BaseModel):
    org_id: str
    service_id: str
    staff_id: Optional[str] = None
    resource_id: Optional[str] = None
    date: str
    duration: int = 60
