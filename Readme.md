# Appointment Booking Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-green.svg)](https://aws.amazon.com/dynamodb/)
[![Stripe](https://img.shields.io/badge/Stripe-Payment-purple.svg)](https://stripe.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, serverless appointment booking system built with Python, AWS Lambda, DynamoDB, and Stripe integration.

## Features

- JWT Authentication - Secure token-based auth with role support
- Smart Availability - Real-time slot calculation based on staff schedules
- Double-Booking Prevention - Atomic DynamoDB writes prevent conflicts
- Stripe Integration - Payment intents, webhooks, and refunds
- Multi-Tenant - Organization isolation via partition keys
- Scalable - Serverless architecture auto-scales with demand

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

## Quick Start

### Prerequisites

- Python 3.11+
- AWS Account
- Stripe Account

### Installation

```bash
# Clone the repository
git clone https://github.com/danyalaltaff11555/OpenSlots-lambda.git
cd appointment-lambda

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

## Project Structure

```
appointment-lambda/
├── src/
│   ├── handlers/          # Lambda handlers
│   │   ├── booking.py
│   │   ├── availability.py
│   │   ├── organization.py
│   │   ├── staff.py
│   │   └── payment.py
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   ├── repositories/      # Data access
│   └── utils/             # Utilities
├── tests/                 # Unit & integration tests
├── docs/                  # Architecture & use cases
├── infrastructure/        # AWS CDK stacks
└── pyproject.toml         # Dependencies
```

## Documentation

- [Architecture](docs/architecture.md) - System design and data models
- [Use Cases](docs/usecases.md) - Business workflows
- [Contributing](CONTRIBUTING.md) - How to contribute

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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /orgs | Create organization |
| GET | /orgs/{id} | Get organization |
| POST | /staff | Add staff member |
| GET | /availability | Query available slots |
| POST | /bookings | Create booking |
| GET | /bookings/{id} | Get booking |
| PATCH | /bookings/{id} | Reschedule booking |
| DELETE | /bookings/{id} | Cancel booking |
| POST | /payments | Create payment |

## Contributing

Contributions are welcome! Please read our Contributing Guide for details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
