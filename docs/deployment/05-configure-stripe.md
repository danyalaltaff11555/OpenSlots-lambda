# Step 5: Configure Stripe Webhook

## Get Your API Endpoint

After deployment, get your API URL:

```bash
cdk deploy LambdaStack --outputs-file outputs.json
cat outputs.json
```

Or from AWS Console:
- **CloudFormation -> LambdaStack -> Outputs**
- Look for `Endpoint` key

## Configure Stripe Dashboard

### 1. Add Webhook Endpoint

1. Go to https://dashboard.stripe.com/test/webhooks
2. Click **Add endpoint**
3. Enter your endpoint URL:
   ```
   https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/payments/webhook
   ```
4. Select **payment_intent.succeeded** event
5. Click **Add endpoint**

### 2. Copy Webhook Secret

After adding, click **Reveal** next to the signing secret:
```
whsec_abc123...
```

Add this to your `.env` file:
```env
STRIPE_WEBHOOK_SECRET=whsec_abc123...
```

### 3. Update Lambda Environment

If using Lambda environment variables for webhook secret:

1. Go to **AWS Console -> Lambda**
2. Select the `PaymentHandler` function
3. Go to **Configuration -> Environment variables**
4. Add `STRIPE_WEBHOOK_SECRET` with your value
5. Click **Save**

## Test Webhook Locally (Optional)

Use Stripe CLI to test webhooks locally:

```bash
# Install Stripe CLI
winget install Stripe.cli

# Login to Stripe
stripe login

# Listen for webhooks
stripe listen --forward-to localhost:3000/webhook
```

## Verify Stripe Configuration

Create a test booking and payment:

```bash
API_URL="https://your-api.execute-api.us-east-1.amazonaws.com/prod"

# 1. Create organization
ORG=$(curl -s -X POST $API_URL/orgs \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Spa", "email": "info@testspa.com"}')
ORG_ID=$(echo $ORG | jq -r '.data.id')

# 2. Create staff member
STAFF=$(curl -s -X POST $API_URL/staff \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "John", "email": "john@testspa.com"}')

# 3. Create a booking
BOOKING=$(curl -s -X POST $API_URL/bookings \
  -H "Content-Type: application/json" \
  -d '{"org_id": "'$ORG_ID'", "staff_id": "staff1", "service_id": "svc1", "start_time": "2025-02-01T10:00:00Z", "customer_email": "customer@email.com", "customer_name": "Customer Name"}')
```

---

## Troubleshooting Stripe Issues

### Webhook Not Received

1. Check **Stripe Dashboard -> Webhooks** for failed deliveries
2. Verify Lambda logs in **CloudWatch**
3. Ensure webhook secret matches

### Payment Intent Failed

1. Use test card numbers from https://stripe.com/docs/testing
2. Common test card: `4242 4242 4242 4242`

---

## Next Steps

Proceed to [Step 6: Testing the Deployment](../06-testing.md)
