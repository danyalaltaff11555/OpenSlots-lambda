import boto3
from typing import Dict, List, Any, Optional
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import config


class DynamoDBRepository:
    _table = None

    def __init__(self, table_name: Optional[str] = None):
        self.table_name = table_name or config.TABLE_NAME

    @property
    def table(self):
        if DynamoDBRepository._table is None:
            DynamoDBRepository._table = boto3.resource(
                "dynamodb", region_name=config.REGION
            ).Table(self.table_name)
        return DynamoDBRepository._table

    def put_item(self, item: Dict[str, Any], condition: Optional[str] = None) -> None:
        kwargs: Dict[str, Any] = {"Item": item}
        if condition:
            kwargs["ConditionExpression"] = condition
        self.table.put_item(**kwargs)

    def get_item(self, pk: str, sk: str) -> Optional[Dict[str, Any]]:
        return self.table.get_item(Key={"PK": pk, "SK": sk}).get("Item")

    def query(
        self, pk: str, sk_prefix: Optional[str] = None, sk_range: Optional[tuple] = None
    ) -> List[Dict]:
        key_cond = Key("PK").eq(pk)
        if sk_prefix:
            key_cond &= Key("SK").begins_with(sk_prefix)
        elif sk_range:
            key_cond &= Key("SK").between(sk_range[0], sk_range[1])
        return self.table.query(KeyConditionExpression=key_cond).get("Items", [])

    def query_index(
        self,
        index_name: str,
        pk: str,
        sk: Optional[str] = None,
        sk_prefix: Optional[str] = None,
    ) -> List[Dict]:
        key_cond = Key("PK").eq(pk)
        if sk:
            key_cond &= Key("SK").eq(sk)
        elif sk_prefix:
            key_cond &= Key("SK").begins_with(sk_prefix)
        return self.table.query(
            IndexName=index_name, KeyConditionExpression=key_cond
        ).get("Items", [])

    def update_item(
        self,
        pk: str,
        sk: str,
        updates: Dict[str, Any],
        condition: Optional[str] = None,
    ) -> None:
        update_expr = "SET " + ", ".join(f"{k} = :{k}" for k in updates)
        kwargs: Dict[str, Any] = {
            "Key": {"PK": pk, "SK": sk},
            "UpdateExpression": update_expr,
            "ExpressionAttributeValues": {f":{k}": v for k, v in updates.items()},
        }
        if condition:
            kwargs["ConditionExpression"] = condition
        self.table.update_item(**kwargs)

    def delete_item(self, pk: str, sk: str) -> None:
        self.table.delete_item(Key={"PK": pk, "SK": sk})

    def atomic_put(self, item: Dict[str, Any]) -> bool:
        try:
            self.put_item(
                item, condition="attribute_not_exists(PK) AND attribute_not_exists(SK)"
            )
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise
