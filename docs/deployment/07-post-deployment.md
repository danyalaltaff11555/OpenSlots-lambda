# Step 7: Post-Deployment

## Configure CloudWatch Alarms

### Create Budget Alert

1. Go to **AWS Console -> Billing -> Budgets**
2. Create budget with:
   - Budget type: **Cost budget**
   - Amount: $10/month (for testing)
   - Alert threshold: 50%, 80%, 100%

### Create Lambda Error Alarm

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "LambdaErrors" \
  --alarm-description "Alert on Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=BookingHandler \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts
```

### Create API Gateway 5xx Alarm

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "API5xxErrors" \
  --alarm-description "Alert on 5xx errors" \
  --metric-name 5XXError \
  --namespace AWS/ApiGateway \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=ApiName,Value=BookingApi \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts
```

## Set Up Custom Domain (Optional)

### Register Domain

1. Go to **Route 53** or your domain registrar
2. Register a domain (e.g., `appointments.yourdomain.com`)

### Create SSL Certificate

```bash
aws acm request-certificate \
  --domain-name "*.yourdomain.com" \
  --validation-method DNS
```

### Configure API Gateway Custom Domain

1. Go to **AWS Console -> API Gateway -> Custom Domain Names**
2. Create custom domain
3. Select ACM certificate
4. Note the CloudFront distribution URL

### Update Route 53

Create A record pointing to CloudFront URL.

## Monitor Costs

### AWS Cost Explorer

1. Go to **AWS Console -> Cost Explorer**
2. Filter by service:
   - Lambda
   - API Gateway
   - DynamoDB
   - CloudWatch

### Expected Costs (Estimate)

| Service | Free Tier | Pay-as-you-go |
|---------|-----------|---------------|
| Lambda | 1M requests | $0.20 per 1M |
| API Gateway | 1M calls | $3.50 per 1M |
| DynamoDB | 25GB storage | $0.25 per GB |
| CloudWatch | 5GB logs | $0.50 per GB |

For low-traffic app: **$5-20/month**

## Security Hardening

### 1. Enable API Throttling

Configure in API Gateway:
- Rate limit: 100 requests/second
- Burst limit: 200 requests

### 2. Enable WAF

1. Go to **AWS Console -> WAF & Shield**
2. Create Web ACL
3. Associate with API Gateway
4. Add rules:
   - AWS managed rules
   - Rate-based rules

### 3. Enable CloudTrail

```bash
aws cloudtrail create-trail \
  --name OpenSlotsTrail \
  --s3-bucket-name your-cloudtrail-bucket \
  --is-multi-region-trail
```

## Backup and Recovery

### DynamoDB Backup

1. Enable point-in-time recovery:
```bash
aws dynamodb update-continuous-backups \
  --table-name appointments \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true
```

### Export to S3

1. Go to **DynamoDB -> Tables -> Exports and imports**
2. Export to S3 bucket

## Update to Production

### Switch from Test to Live Stripe Keys

```env
# In .env
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_WEBHOOK_SECRET=whsec_live_your_webhook_secret
```

### Redeploy with Production Config

```bash
# Update environment variables in CDK
# Redeploy
cdk deploy LambdaStack
```

### Update API Gateway Stage

1. Go to **API Gateway -> Stages -> prod**
2. Enable **API cache**
3. Configure throttling

---

## Maintenance

### Regular Tasks

| Task | Frequency |
|------|-----------|
| Review CloudWatch logs | Weekly |
| Check billing dashboard | Monthly |
| Rotate secrets | Quarterly |
| Update dependencies | Monthly |

### Update Lambda Runtime

Monitor Python version support:
- https://docs.aws.amazon.com/lambda/latest/dg/runtime-support-policy.html

Update runtime when needed:
```bash
# Update in infrastructure/lambdas.py
runtime=_lambda.Runtime.PYTHON_3_12  # When available

cdk deploy
```

---

## Troubleshooting

### 502 Bad Gateway

- Check Lambda logs in CloudWatch
- Increase Lambda timeout
- Check memory allocation

### 429 Too Many Requests

- Enable throttling in API Gateway
- Implement client-side retry

### Lambda Cold Starts

- Increase memory allocation (more CPU = faster)
- Use provisioned concurrency for critical endpoints
