import json
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4
from utils.response import success_response, error_response
from utils.auth import validate_token, extract_token
from repositories.dynamodb_repository import DynamoDBRepository


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        repo = DynamoDBRepository()
        auth_header = event.get("headers", {}).get("Authorization", "")
        token = extract_token(auth_header)
        payload = validate_token(token)
        org_id = payload.org_id

        method = event.get("httpMethod", "")
        path = event.get("path", "")
        path_params = event.get("pathParameters", {}) or {}

        if method == "POST" and "/staff" in path:
            body = json.loads(event.get("body", "{}"))
            staff_id = str(uuid4())[:8]
            staff = {
                "PK": f"ORG#{org_id}",
                "SK": f"STAFF#{staff_id}",
                "id": staff_id,
                "entity_type": "staff",
                "org_id": org_id,
                "name": body.get("name"),
                "email": body.get("email"),
                "phone": body.get("phone"),
                "role": body.get("role", "staff"),
                "services": body.get("services", []),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            repo.put_item(staff)
            return success_response(staff, status_code=201)

        if method == "GET" and path == f"/orgs/{org_id}/staff":
            return success_response(repo.query(f"ORG#{org_id}", "STAFF#"))

        if method == "GET" and "/staff/" in path:
            staff_id = path_params.get("id")
            if not staff_id:
                return error_response("Staff ID required", status_code=400)
            staff = repo.get_item(f"ORG#{org_id}", f"STAFF#{staff_id}")
            if not staff:
                return error_response("Staff not found", status_code=404)
            return success_response(staff)

        if method == "PATCH" and "/staff/" in path:
            staff_id = path_params.get("id")
            if not staff_id:
                return error_response("Staff ID required", status_code=400)
            body = json.loads(event.get("body", "{}"))
            allowed = ["name", "email", "phone", "role", "services"]
            updates = {k: v for k, v in body.items() if k in allowed}
            updates["updated_at"] = datetime.utcnow().isoformat()
            repo.update_item(f"ORG#{org_id}", f"STAFF#{staff_id}", updates)
            return success_response(repo.get_item(f"ORG#{org_id}", f"STAFF#{staff_id}"))

        if method == "DELETE" and "/staff/" in path:
            staff_id = path_params.get("id")
            if not staff_id:
                return error_response("Staff ID required", status_code=400)
            repo.delete_item(f"ORG#{org_id}", f"STAFF#{staff_id}")
            return success_response({"deleted": True})

        return error_response("Method not allowed", status_code=405)

    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(str(e), status_code=400)
