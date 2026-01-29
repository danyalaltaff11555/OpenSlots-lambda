import json
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4
from utils.response import success_response, error_response
from repositories.dynamodb_repository import DynamoDBRepository


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        repo = DynamoDBRepository()
        method = event.get("httpMethod", "")
        path = event.get("path", "")
        path_params = event.get("pathParameters", {}) or {}

        if method == "POST" and path == "/orgs":
            body = json.loads(event.get("body", "{}"))
            org_id = str(uuid4())[:8]
            org = {
                "PK": f"ORG#{org_id}",
                "SK": f"ORG#{org_id}",
                "id": org_id,
                "entity_type": "organization",
                "name": body.get("name"),
                "email": body.get("email"),
                "timezone": body.get("timezone", "UTC"),
                "business_hours": body.get("business_hours", {}),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            repo.put_item(org)
            return success_response(org, status_code=201)

        if method == "GET" and "/orgs/" in path:
            org_id = path_params.get("id")
            if not org_id:
                return error_response("Organization ID required", status_code=400)
            org = repo.get_item(f"ORG#{org_id}", f"ORG#{org_id}")
            if not org:
                return error_response("Organization not found", status_code=404)
            return success_response(org)

        if method == "PATCH" and "/orgs/" in path:
            org_id = path_params.get("id")
            if not org_id:
                return error_response("Organization ID required", status_code=400)
            body = json.loads(event.get("body", "{}"))
            allowed = ["name", "email", "timezone", "business_hours"]
            updates = {k: v for k, v in body.items() if k in allowed}
            updates["updated_at"] = datetime.utcnow().isoformat()
            repo.update_item(f"ORG#{org_id}", f"ORG#{org_id}", updates)
            return success_response(repo.get_item(f"ORG#{org_id}", f"ORG#{org_id}"))

        return error_response("Method not allowed", status_code=405)

    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(str(e), status_code=400)
