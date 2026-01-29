# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                              │
│  (Lambda Handler Functions)                                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Business Logic Layer                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │  Booking    │ │ Availability│ │  Payment    │               │
│  │  Service    │ │  Service    │ │  Service    │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│  ┌─────────────┐ ┌─────────────┐                                │
│  │ Cancellation│ │  ...        │                                │
│  │ Service     │ │             │                                │
│  └─────────────┘ └─────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Access Layer                            │
│                    DynamoDB Repository                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DynamoDB                                 │
│  Single Table with GSIs                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Clean Architecture Layers

### Handlers (API Layer)
- HTTP request/response handling
- Authentication/authorization
- Input validation

### Services (Business Logic)
- Booking management
- Availability calculation
- Payment processing
- Cancellation policies

### Repositories (Data Access)
- DynamoDB operations
- Query patterns
- Atomic transactions

### Models (Domain)
- Organization, Staff, Service, Resource, Booking, Payment
- Data validation

## DynamoDB Schema

### Primary Key Design
```
PK: ORG#{org_id}          # Partition Key
SK: ENTITY#{type}#{id}    # Sort Key
```

### Entity Types
- `ORG#` - Organization
- `STAFF#` - Staff member
- `BOOKING#` - Booking
- `SERVICE#` - Service
- `RESOURCE#` - Resource
- `PAYMENT#` - Payment
- `SCHEDULE#` - Staff schedule

### Global Secondary Indexes
- `BookingsByDateIndex` - Query bookings by date

## API Flow

### Booking Creation
```
1. Customer → GET /availability → Query available slots
2. Customer → POST /bookings → Create pending booking
3. System → Atomic write → Prevent double-booking
4. Customer → POST /payments → Create Stripe payment intent
5. Stripe → Webhook → Confirm payment
6. System → Update booking → Set status to "confirmed"
```

## Security

- JWT-based authentication
- Tenant isolation via org_id
- Role-based access (admin, staff, customer)
- API Gateway for rate limiting

## Scalability

- AWS Lambda for compute (auto-scaling)
- DynamoDB for managed NoSQL
- Connection pooling via lazy initialization
- Stateless handlers
