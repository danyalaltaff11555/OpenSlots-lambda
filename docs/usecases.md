# Use Cases

## 1. Organization Setup
**Actor:** Business Owner

**Preconditions:**
- None

**Main Flow:**
1. Create organization via `POST /orgs`
2. Configure business hours
3. Add staff members via `POST /staff`
4. Define services via `POST /orgs/{id}/services`
5. Add resources (rooms, equipment) via `POST /orgs/{id}/resources`

## 2. Customer Booking
**Actor:** Customer

**Preconditions:**
- Organization, services, and staff configured

**Main Flow:**
1. Query availability via `GET /availability?service_id=...&date=...`
2. Select available time slot
3. Create booking via `POST /bookings`
4. Complete payment via `POST /payments`
5. Receive confirmation email/SMS

## 3. Staff Schedule Management
**Actor:** Staff Member / Admin

**Preconditions:**
- Staff member added to organization

**Main Flow:**
1. Set weekly schedule via `POST /staff/{id}/schedules`
2. Add time-off/vacation
3. View bookings via `GET /bookings`

## 4. Booking Management
**Actor:** Staff / Admin

**Main Flow:**
1. View booking details via `GET /bookings/{id}`
2. Reschedule via `PATCH /bookings/{id}` with new start_time
3. Cancel via `DELETE /bookings/{id}`
4. Apply no-show policy if applicable

## 5. Payment Processing
**Actor:** System / Customer

**Main Flow:**
1. Create payment intent on booking
2. Customer completes payment
3. Stripe webhook confirms payment
4. Booking status updated to "confirmed"
5. Refund processed on cancellation per policy
