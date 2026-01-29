<div align="center">

# OpenSlots Lambda

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-green.svg)](https://aws.amazon.com/dynamodb/)
[![Stripe](https://img.shields.io/badge/Stripe-Payment-purple.svg)](https://stripe.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### A production-ready, serverless appointment booking system

</div>

## About

OpenSlots is a serverless appointment booking platform built with Python, AWS Lambda, DynamoDB, and Stripe. It provides a complete solution for managing appointments, staff schedules, and payments.

### Key Features

- **JWT Authentication** - Secure token-based auth with role support
- **Real-time Availability** - Smart slot calculation based on staff schedules
- **Double-Booking Prevention** - Atomic DynamoDB writes prevent conflicts
- **Stripe Integration** - Payment intents, webhooks, and refunds
- **Multi-Tenant** - Organization isolation via partition keys
- **Serverless** - Auto-scales with demand

---

## Quick Start

### Prerequisites

- Python 3.11+
- AWS Account
- Stripe Account

### Installation

```bash
# Clone the repository
git clone https://github.com/danyalaltaff11555/OpenSlots-lambda.git
cd OpenSlots-lambda

# Install dependencies
poetry install --with infra

# Configure environment
cp .env.example .env
# Edit .env with your AWS and Stripe credentials

# Run tests
pytest tests/ -v
```

### Deployment

```bash
cd infrastructure
cdk deploy
```

---

## Architecture

```
+-----------------+     +-----------------+     +-----------------+
|   API Gateway   |---->|  Lambda Layers  |---->|    DynamoDB     |
|  (REST API)     |     |  (Handlers)     |     |  (Single Table) |
+-----------------+     +-----------------+     +-----------------+
                              |
                              v
                     +-----------------+
                     |     Stripe      |
                     |   (Payments)    |
                     +-----------------+
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Runtime | Python 3.11+ |
| Compute | AWS Lambda |
| API | Amazon API Gateway |
| Database | Amazon DynamoDB |
| Infrastructure | AWS CDK |
| Payments | Stripe |
| Auth | JWT |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orgs` | Create organization |
| `GET` | `/orgs/{id}` | Get organization |
| `POST` | `/staff` | Add staff member |
| `GET` | `/availability` | Query available slots |
| `POST` | `/bookings` | Create booking |
| `GET` | `/bookings/{id}` | Get booking |
| `PATCH` | `/bookings/{id}` | Reschedule booking |
| `DELETE` | `/bookings/{id}` | Cancel booking |
| `POST` | `/payments` | Create payment |

---

## Documentation

- [Architecture](docs/architecture.md) - System design and data models
- [Use Cases](docs/usecases.md) - Business workflows
- [Contributing](CONTRIBUTING.md) - How to contribute

---

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
