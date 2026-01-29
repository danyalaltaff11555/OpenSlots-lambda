from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class Staff:
    id: str
    org_id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: str = "staff"
    services: List[str] = field(default_factory=list)
    schedules: List[Dict] = field(default_factory=list)
    time_off: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StaffSchedule:
    staff_id: str
    day_of_week: int
    start_time: str
    end_time: str
    is_active: bool = True
