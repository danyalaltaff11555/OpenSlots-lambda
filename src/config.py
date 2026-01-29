import os

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "appointments")
REGION = os.environ.get("AWS_REGION", "us-east-1")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-key")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24
