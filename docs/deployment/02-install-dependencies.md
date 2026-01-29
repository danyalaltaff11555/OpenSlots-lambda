# Step 2: Install Dependencies

## Install Python 3.11+

Download from https://www.python.org/downloads/

Verify installation:
```bash
python --version
# Should show Python 3.11.x
```

## Install Node.js 18+

Download from https://nodejs.org/ (LTS version)

Verify installation:
```bash
node --version
# Should show v18.x or higher
npm --version
```

## Install AWS CDK

```bash
npm install -g aws-cdk
```

Verify installation:
```bash
cdk --version
# Should show 2.x
```

## Install Poetry (Python Package Manager)

### Windows

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Linux/macOS

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add Poetry to PATH:
```bash
# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:APPDATA\Python\Scripts", "User")

# Linux/macOS
export PATH="$HOME/.local/bin:$PATH"
```

Verify installation:
```bash
poetry --version
```

## Clone the Repository

```bash
git clone https://github.com/danyalaltaff11555/OpenSlots-lambda.git
cd OpenSlots-lambda
```

## Install Project Dependencies

```bash
# Install all dependencies including infrastructure
poetry install --with infra

# Activate virtual environment
poetry shell
```

Or using pip:

```bash
pip install -r requirements.txt -r dev-requirements.txt
```

## Verify Installation

```bash
# Check Python packages
pip list

# Should show:
# boto3, stripe, pydantic, PyJWT
# aws-cdk-lib, constructs

# Run tests
pytest tests/ -v
```

## Bootstrap AWS CDK

Bootstrap your AWS account for CDK:

```bash
cdk bootstrap
```

This creates:
- S3 bucket for CDK assets
- ECR repository for Docker images
- IAM roles for deployment

---

## Troubleshooting

### Poetry not found after installation

Restart your terminal or run:
```bash
source ~/.bashrc  # Linux/macOS
refreshenv        # Windows (ConEmu/CMDER)
```

### AWS CDK bootstrap fails

Ensure your AWS credentials are configured:
```bash
aws configure
# or
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

---

## Next Steps

Proceed to [Step 3: Configure Environment](../03-configure-environment.md)
