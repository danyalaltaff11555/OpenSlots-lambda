from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class Service:
    id: str
    org_id: str
    name: str
    duration: int
    price: float
    currency: str = "USD"
    description: Optional[str] = None
    staff_required: List[str] = field(default_factory=list)
    resources_required: List[str] = field(default_factory=list)
    buffer_time: int = 0
    preparation_time: int = 0
    is_active: bool = True
    cancellation_policy: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Resource:
    id: str
    org_id: str
    name: str
    type: str
    description: Optional[str] = None
    capacity: int = 1
    services: List[str] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
