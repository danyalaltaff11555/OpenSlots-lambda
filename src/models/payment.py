from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class Payment:
    id: str
    booking_id: str
    org_id: str
    amount: float
    currency: str = "USD"
    stripe_payment_intent_id: Optional[str] = None
    stripe_charge_id: Optional[str] = None
    status: str = "pending"
    refund_id: Optional[str] = None
    refund_amount: float = 0.0
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


PAYMENT_STATUS = ["pending", "succeeded", "failed", "refunded", "partially_refunded"]
