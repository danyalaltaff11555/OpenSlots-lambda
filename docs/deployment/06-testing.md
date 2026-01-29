# Step 6: Testing the Deployment

## Run Unit Tests

```bash
# Activate virtual environment
poetry shell

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_booking_service.py -v
```

## API Integration Testing

### Get Your API Endpoint

```bash
API_URL="https://abc123.execute-api.us-east-1.amazonaws.com/prod"
```

### 1. Create Organization

```bash
curl -s -X POST $API_URL/orgs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Wellness Center",
    "email": "contact@wellness.com",
    "timezone": "America/New_York",
    "business_hours": {
      "0": {"start": "09:00", "end": "18:00"},
      "1": {"start": "09:00", "end": "18:00"},
      "2": {"start": "09:00", "end": "18:00"},
      "3": {"start": "09:00", "end": "18:00"},
      "4": {"start": "09:00", "end": "18:00"},
      "5": {"start": "10:00", "end": "16:00"},
      "6": {"start": "10:00", "end": "14:00"}
    }
  }' | jq .
```

Response:
```json
{
  "data": {
    "id": "abc12345",
    "name": "My Wellness Center",
    ...
  }
}
```

Save the `org_id` for next steps.

### 2. Query Availability

```bash
ORG_ID="your-org-id"

curl -s "$API_URL/availability?org_id=$ORG_ID&service_id=massage&date=2025-02-01&duration=60" | jq .
```

### 3. Create Booking

```bash
ORG_ID="your-org-id"

curl -s -X POST $API_URL/bookings \
  -H "Content-Type: application/json" \
  -d "{
    \"org_id\": \"$ORG_ID\",
    \"staff_id\": \"staff123\",
    \"service_id\": \"massage\",
    \"start_time\": \"2025-02-01T10:00:00Z\",
    \"customer_email\": \"customer@email.com\",
    \"customer_name\": \"John Doe\",
    \"customer_phone\": \"+1234567890\",
    \"amount\": 100.00
  }" | jq .
```

### 4. Get Booking Details

```bash
BOOKING_ID="your-booking-id"

curl -s "$API_URL/bookings/$BOOKING_ID" | jq .
```

### 5. Cancel Booking

```bash
BOOKING_ID="your-booking-id"

curl -s -X DELETE "$API_URL/bookings/$BOOKING_ID" | jq .
```

## Test Error Handling

### Invalid Organization

```bash
curl -s "$API_URL/orgs/invalid-id" | jq .
# Should return 404
```

### Double Booking Prevention

Create two simultaneous bookings for the same slot - second should fail.

---

## Monitor in CloudWatch

1. Go to **AWS Console -> CloudWatch -> Logs**
2. Find log groups:
   - `/aws/lambda/BookingHandler`
   - `/aws/lambda/AvailabilityHandler`
   - `/aws/lambda/PaymentHandler`
3. Search for errors

---

## Next Steps

Proceed to [Step 7: Post-Deployment](../07-post-deployment.md)
