# Step 1: AWS Account Setup

## Prerequisites

Before deploying OpenSlots, ensure you have:

1. **AWS Account** - Sign up at https://aws.amazon.com/
2. **AWS CLI** - Install from https://aws.amazon.com/cli/
3. **Node.js** - Version 18+ required for AWS CDK
4. **Python 3.11+** - Required for the application

## AWS CLI Configuration

```bash
# Install AWS CLI (Windows)
winget install Amazon.AWSCLI

# Or use installer from AWS website
# https://aws.amazon.com/cli/
```

### Configure AWS Credentials

```bash
aws configure
```

Enter your credentials:
- **AWS Access Key ID**: From IAM user
- **AWS Secret Access Key**: From IAM user
- **Default region name**: e.g., `us-east-1`
- **Default output format**: `json`

### Verify Configuration

```bash
aws sts get-caller-identity
```

Should return your account ID and user ARN.

## Create IAM User for CDK

For security, create a dedicated IAM user for CDK deployment:

1. Go to **AWS Console -> IAM -> Users -> Add users**
2. User name: `cdk-deploy-user`
3. Access type: **Programmatic access**
4. Attach policies:
   - `AdministratorAccess` (for initial setup)
   - Or create custom policies with minimal permissions
5. Save the Access Key and Secret Key

## Required AWS Services

OpenSlots uses these AWS services:

| Service | Purpose |
|---------|---------|
| **Lambda** | Compute for API handlers |
| **API Gateway** | REST API endpoint |
| **DynamoDB** | Database for all data |
| **IAM** | Roles and permissions |
| **CloudWatch** | Logging and monitoring |
| **Secrets Manager** | Store Stripe keys |
| **Parameter Store** | Environment variables |

## AWS Region Selection

Choose a region close to your users:

- **us-east-1** (N. Virginia) - Most services, often cheapest
- **us-west-2** (Oregon) - Popular alternative
- **eu-west-1** (Ireland) - For European users

Set the region in your `.env` file:

```env
AWS_REGION=us-east-1
```

---

## Next Steps

Proceed to [Step 2: Install Dependencies](../02-install-dependencies.md)
