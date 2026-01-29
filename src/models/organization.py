from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class Organization:
    id: str
    name: str
    email: str
    timezone: str = "UTC"
    business_hours: Dict[str, Dict[str, str]] = field(default_factory=dict)
    cancellation_policy: Dict[str, any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
