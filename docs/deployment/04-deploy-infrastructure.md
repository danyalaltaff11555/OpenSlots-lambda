# Step 4: Deploy Infrastructure

## Navigate to Infrastructure Directory

```bash
cd infrastructure
```

## Review the Stack

Before deploying, review what will be created:

```bash
cdk list
# Should show:
# DynamoDBStack
# LambdaStack
```

## Synthesize CloudFormation Template

```bash
cdk synth
```

This generates the CloudFormation template without deploying. Review the output for any issues.

## Deploy the Stacks

### Deploy DynamoDB Stack First

```bash
cdk deploy DynamoDBStack
```

This creates:
- DynamoDB table `appointments`
- Global Secondary Indexes

### Deploy Lambda Stack

```bash
cdk deploy LambdaStack
```

This creates:
- Lambda functions for each handler
- API Gateway REST API
- IAM roles and permissions
- CloudWatch Log groups

## Deployment Output

After deployment, you'll see output like:

```
LambdaStack.Endpoint = https://abc123.execute-api.us-east-1.amazonaws.com/prod/
```

Copy this URL - it's your API endpoint.

## Test the API

```bash
# Replace with your endpoint
API_URL="https://abc123.execute-api.us-east-1.amazonaws.com/prod"

# Test health check (create organization)
curl -X POST $API_URL/orgs \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Business", "email": "test@example.com"}'
```

## View in AWS Console

1. Go to **AWS Console -> CloudFormation**
2. You should see `DynamoDBStack` and `LambdaStack`
3. Check the **Resources** tab to see created resources

## Common Issues

### Access Denied

Ensure your AWS credentials have sufficient permissions:
- `IAMFullAccess` or custom IAM permissions
- `AmazonDynamoDBFullAccess`
- `AmazonAPIGatewayAdministrator`

### Stack Already Exists

If redeploying and stack exists:
```bash
cdk deploy --force
```

---

## Next Steps

Proceed to [Step 5: Configure Stripe Webhook](../05-configure-stripe.md)
