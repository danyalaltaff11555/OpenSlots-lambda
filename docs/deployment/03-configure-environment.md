# Step 3: Configure Environment

## Copy Environment Template

```bash
cp .env.example .env
```

## Configure Environment Variables

Edit `.env` file with your values:

```env
# AWS Configuration
AWS_REGION=us-east-1
DYNAMODB_TABLE=appointments

# JWT Authentication (Generate a secure random key)
JWT_SECRET=your-super-secret-jwt-key-min-32-chars

# Stripe Configuration (Get from Stripe Dashboard)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Optional: Custom domain
# CUSTOM_DOMAIN=api.yourdomain.com
```

## Generate Secure JWT Secret

Generate a strong random secret:

```bash
# Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Output: a1b2c3d4e5f6...
```

## Configure Stripe

### 1. Get Stripe Keys

1. Go to https://dashboard.stripe.com/test/apikeys
2. Copy **Test** secret key (starts with `sk_test_`)
3. Copy **Test** publishable key (starts with `pk_test_`)

### 2. Configure Webhook

1. Go to https://dashboard.stripe.com/test/webhooks
2. Add endpoint: `https://your-api.execute-api.us-east-1.amazonaws.com/prod/payments/webhook`
3. Select events: `payment_intent.succeeded`
4. Copy the webhook secret (starts with `whsec_`)

### 3. Update .env

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Configure AWS Secrets (Optional)

For production, store secrets in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name OpenSlots/JWTSecret \
  --secret-string "your-jwt-secret"

aws secretsmanager create-secret \
  --name OpenSlots/StripeSecret \
  --secret-string "sk_test_..."
```

Update Lambda environment variables in CDK stack to reference secrets.

## Verify Configuration

```bash
# Test configuration
python -c "from dotenv import load_dotenv; load_dotenv(); print('Config loaded successfully')"
```

---

## Security Best Practices

1. **Never commit .env to git**
2. **Use different keys for test and production**
3. **Rotate secrets periodically**
4. **Use IAM roles instead of access keys where possible**

---

## Next Steps

Proceed to [Step 4: Deploy Infrastructure](../04-deploy-infrastructure.md)
