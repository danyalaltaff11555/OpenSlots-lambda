import json
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_event(event_type: str, data: Dict[str, Any]) -> None:
    logger.info(
        json.dumps(
            {
                "event_type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    )
