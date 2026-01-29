# Deployment Guide

Complete step-by-step guide to deploy OpenSlots to AWS.

## Prerequisites

- AWS Account
- Stripe Account
- GitHub Account (for CI/CD)

## Deployment Steps

| Step | Title | Description |
|------|-------|-------------|
| 1 | [AWS Account Setup](01-aws-account-setup.md) | Configure AWS account and IAM user |
| 2 | [Install Dependencies](02-install-dependencies.md) | Install Python, Node.js, CDK, Poetry |
| 3 | [Configure Environment](03-configure-environment.md) | Set up environment variables and secrets |
| 4 | [Deploy Infrastructure](04-deploy-infrastructure.md) | Deploy DynamoDB, Lambda, API Gateway |
| 5 | [Configure Stripe](05-configure-stripe.md) | Set up Stripe webhooks and payments |
| 6 | [Testing](06-testing.md) | Test APIs and verify deployment |
| 7 | [Post-Deployment](07-post-deployment.md) | Monitoring, security, and maintenance |

## Quick Reference

```bash
# Clone and install
git clone https://github.com/danyalaltaff11555/OpenSlots-lambda.git
cd OpenSlots-lambda
poetry install --with infra

# Configure
cp .env.example .env
# Edit .env with your credentials

# Deploy
cd infrastructure
cdk bootstrap
cdk deploy

# Test
pytest tests/ -v
```

## Estimated Costs

| Service | Free Tier | Estimated Cost |
|---------|-----------|----------------|
| Lambda | 1M requests/month | $5-15/month |
| API Gateway | 1M calls/month | $3-10/month |
| DynamoDB | 25GB storage | $5-15/month |
| CloudWatch | 5GB logs | $2-5/month |
| **Total** | | **$15-45/month** |

## Architecture Overview

```
User → API Gateway → Lambda → DynamoDB
              ↓
         Stripe (Payments)
```

## Support

- Documentation: [README](../README.md)
- Architecture: [architecture.md](../architecture.md)
- Use Cases: [usecases.md](../usecases.md)
- Contributing: [CONTRIBUTING.md](../CONTRIBUTING.md)

## Common Issues

See [Step 7: Post-Deployment](07-post-deployment.md) for troubleshooting.
