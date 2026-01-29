from typing import Any, Dict
import json


def success_response(data: Any, status_code: int = 200) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"data": data}),
    }


def error_response(message: str, status_code: int = 500) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": {"message": message}}),
    }
