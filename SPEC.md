# SPEC.md - Elder Care Assistant Specification Kit

Complete technical specification for the Elder Care Assistant platform.

**Version**: 1.0.0  
**Last Updated**: 2026-06-09  
**Status**: Active Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [System Architecture](#system-architecture)
4. [Functional Requirements](#functional-requirements)
5. [Data Specifications](#data-specifications)
6. [API Specifications](#api-specifications)
7. [Security Specifications](#security-specifications)
8. [Performance Requirements](#performance-requirements)
9. [Deployment Specifications](#deployment-specifications)
10. [Testing Specifications](#testing-specifications)
11. [Compliance Requirements](#compliance-requirements)

---

## Executive Summary

### Project Vision

Develop an AI-powered health monitoring and companion system that enables elderly individuals to receive personalized care support while maintaining family connectivity and emergency responsiveness.

### Key Objectives

- Provide 24/7 AI-powered chat companion
- Enable health monitoring and medication management
- Facilitate family communication and updates
- Ensure quick emergency response capabilities
- Maintain strict privacy and security standards
- Support accessibility for elderly users

### Target Users

- **Primary**: Elderly individuals (65+)
- **Secondary**: Family members, caregivers
- **Tertiary**: Healthcare providers (future)

### Success Metrics

- 95%+ system uptime
- <2 second API response time (p95)
- 80%+ medication adherence (where tracked)
- <5 minute family notification time
- 99%+ data security compliance

---

## Project Overview

### Scope

**In Scope**:
- User authentication and authorization
- Health monitoring and tracking
- Medication reminder system
- AI-powered chat interface
- Family member connectivity
- Emergency alert system
- User management and settings
- Health data analytics

**Out of Scope** (Future Releases):
- Direct healthcare provider integration
- Prescription management system
- Telehealth video calls
- Wearable device integration
- Advanced analytics and ML models
- Mobile app (web-first approach)

### Constraints

**Technical**:
- Must support Python 3.9+
- PostgreSQL for data persistence
- Redis for caching/sessions
- FastAPI framework
- Claude API for AI features

**Business**:
- Budget-conscious implementation
- MVP launch in Q3 2026
- Healthcare compliance (HIPAA in US, GDPR in EU)
- Scalable to 100,000+ users

**Timeline**:
- Phase 1 (Current): Core features - 4 weeks
- Phase 2: Family features - 3 weeks
- Phase 3: Emergency/advanced - 2 weeks
- Phase 4: Testing/polish - 2 weeks

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│           Frontend (React/Vue)                  │
│  - Web browser (Chrome, Firefox, Safari, Edge)  │
│  - Responsive design for elderly users          │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS
┌──────────────────▼──────────────────────────────┐
│         FastAPI Backend Server                  │
│  ┌──────────────────────────────────────────┐   │
│  │ API Routes                               │   │
│  │ - /api/v1/auth                          │   │
│  │ - /api/v1/health                        │   │
│  │ - /api/v1/chat                          │   │
│  │ - /api/v1/reminders                     │   │
│  │ - /api/v1/family                        │   │
│  │ - /api/v1/emergency                     │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ Middleware                               │   │
│  │ - Authentication (JWT)                  │   │
│  │ - Error Handling                        │   │
│  │ - CORS                                  │   │
│  │ - Rate Limiting                         │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ Services                                 │   │
│  │ - AuthService                           │   │
│  │ - HealthService                         │   │
│  │ - ChatService (Claude integration)      │   │
│  │ - ReminderService                       │   │
│  │ - FamilyService                         │   │
│  │ - EmergencyService                      │   │
│  └──────────────────────────────────────────┘   │
└──────────┬──────────────────────────────────────┘
           │
    ┌──────┴────────┬────────────────┬────────┐
    │               │                │        │
┌───▼───┐      ┌───▼────┐     ┌───▼──┐  ┌───▼────┐
│  PG   │      │ Redis  │     │Claude│  │Twilio  │
│  DB   │      │ Cache  │     │ API  │  │(SMS)   │
└───────┘      └────────┘     └──────┘  └────────┘
```

### Technology Stack

**Backend**:
- Framework: FastAPI 0.104+
- Language: Python 3.9+
- ORM: SQLAlchemy 2.0+
- Async: asyncio + uvicorn
- Validation: Pydantic v2
- Database: PostgreSQL 12+
- Cache: Redis 6.0+

**Infrastructure**:
- Server: Ubuntu 20.04 LTS
- Web Server: Nginx (reverse proxy)
- SSL: Let's Encrypt (HTTPS)
- Monitoring: Prometheus + Grafana (future)
- Logging: ELK Stack (future)

**External Services**:
- Claude API (Anthropic)
- SMTP (email notifications)
- Twilio (SMS notifications - optional)
- SendGrid (optional alternative)

**Development**:
- Version Control: Git
- Package Manager: pip + requirements.txt
- Testing: pytest
- Code Quality: pylint, flake8, black
- Documentation: Markdown + Sphinx

---

## Functional Requirements

### FR1: User Authentication

**Requirement**: System must support secure user registration and login

**Details**:
- Email/password registration
- JWT-based authentication
- Token expiration: 30 minutes
- Refresh token expiration: 7 days
- Optional 2FA (SMS or email)
- Password reset via email
- Account lockout after 5 failed attempts
- Session timeout: 1 hour inactivity

**Acceptance Criteria**:
- ✓ New users can register with email
- ✓ Users can login with credentials
- ✓ Tokens expire after 30 minutes
- ✓ Refresh tokens work for 7 days
- ✓ Failed login attempts blocked after 5 tries

### FR2: User Profile Management

**Requirement**: Users can manage their profile and preferences

**Details**:
- Profile fields: name, email, phone, age, medical conditions
- Emergency contacts: up to 5 contacts with relationships
- Medication history
- Notification preferences
- Privacy settings
- Language preference (future: multi-language support)

**Acceptance Criteria**:
- ✓ Users can view/edit profile
- ✓ Can add/edit/remove emergency contacts
- ✓ Can list current medications
- ✓ Can set notification preferences

### FR3: Daily Health Check-In

**Requirement**: Users can submit daily health information

**Details**:
- Fields: mood (1-10), energy (1-10), sleep quality (1-10), symptoms, notes
- Timestamp: auto-captured server-side
- Optional: blood pressure, heart rate, weight, temperature
- Historical tracking: view past 30 days
- Trend analysis: simple patterns (mood going up/down)

**Acceptance Criteria**:
- ✓ Users can submit daily check-in
- ✓ Data is timestamped and persisted
- ✓ Can view check-in history
- ✓ Can see 30-day trend charts

### FR4: Medication Reminders

**Requirement**: System sends medication reminders at specified times

**Details**:
- Create reminder with: medication name, dosage, frequency, time
- Frequencies: once daily, twice daily, custom schedule
- Notification channels: in-app, email, SMS (optional)
- Reminder history: track which were confirmed
- Adherence tracking: calculate percentage taken

**Acceptance Criteria**:
- ✓ Users can create medication reminders
- ✓ Reminders notify at correct time
- ✓ Users can mark as "taken"
- ✓ Can view adherence history

### FR5: AI Chat Companion

**Requirement**: 24/7 AI-powered chat interface using Claude

**Details**:
- Integration with Claude API
- Conversation history stored securely
- Model: claude-3-5-sonnet-20241022 (configurable)
- Response time: <5 seconds (p95)
- Context awareness: can reference health data (with consent)
- Medical disclaimer always present
- Session management: separate chats, not mixed

**Acceptance Criteria**:
- ✓ Users can send messages
- ✓ AI responds with relevant answers
- ✓ Chat history is persisted
- ✓ Medical disclaimer displayed
- ✓ Response time <5 seconds

### FR6: Family Member Connectivity

**Requirement**: Enable authorized family members to receive updates

**Details**:
- Add family members by email invitation
- Set permissions: view health, view reminders, messaging
- Family receives notifications on health status changes
- Can send messages to primary user
- View read-only dashboard of user's status
- No editing permissions for family (read-only)

**Acceptance Criteria**:
- ✓ Can invite family by email
- ✓ Invitations work and tracked
- ✓ Family can view permitted data
- ✓ Family receives notifications
- ✓ Messaging works bidirectionally

### FR7: Emergency Alert System

**Requirement**: Quick access to emergency features

**Details**:
- SOS button prominently displayed
- When triggered: alert emergency contacts immediately
- Include: user location (if available), emergency info
- Contact methods: email, SMS, phone call (Twilio)
- Emergency contact list: up to 10 contacts
- Medical alert information: allergies, blood type, meds

**Acceptance Criteria**:
- ✓ SOS button visible and functional
- ✓ Emergency contacts alerted within 2 minutes
- ✓ Can add/edit emergency contacts
- ✓ Medical info displays in emergency

### FR8: Health Data Analytics

**Requirement**: Basic analytics and insights on health data

**Details**:
- Trend analysis: mood, energy, sleep over 7/30/90 days
- Pattern detection: identify common times for issues
- Suggestions: based on patterns ("You're usually tired on Mondays")
- Export: can download health data as CSV
- No personally identifiable AI analysis (local only)

**Acceptance Criteria**:
- ✓ Can view trend charts
- ✓ System suggests patterns
- ✓ Can export health data
- ✓ Insights are accurate and relevant

### FR9: Notification System

**Requirement**: Flexible notification delivery across channels

**Details**:
- Channels: In-app, Email, SMS (Twilio - optional), Browser push (future)
- Types: reminders, family updates, health alerts, system notifications
- Preferences: users control what/when to receive
- Delivery retry: 3 attempts with exponential backoff
- Rate limiting: max 5 notifications per hour per user

**Acceptance Criteria**:
- ✓ In-app notifications work
- ✓ Email notifications sent
- ✓ SMS optional and configurable
- ✓ Users can disable notifications
- ✓ No spam (rate limited)

### FR10: Account Management

**Requirement**: Users can manage their account lifecycle

**Details**:
- Password change: required strong passwords
- Account deletion: soft delete (anonymize after 90 days)
- Data export: GDPR-compliant data export
- Session management: view/logout other sessions
- Login history: see recent logins with IP/device

**Acceptance Criteria**:
- ✓ Users can change password
- ✓ Can delete account
- ✓ Can export personal data
- ✓ Can view login history

---

## Data Specifications

### Data Models

#### User

```python
class User:
    id: int (PK)
    email: str (UNIQUE, NOT NULL)
    phone: str (OPTIONAL)
    first_name: str (NOT NULL)
    last_name: str (NOT NULL)
    date_of_birth: date (OPTIONAL)
    gender: enum ['M', 'F', 'Other', 'Prefer not to say'] (OPTIONAL)
    password_hash: str (NOT NULL)
    is_active: bool (DEFAULT True)
    created_at: datetime (DEFAULT now)
    updated_at: datetime (DEFAULT now)
    last_login: datetime (OPTIONAL)
    
    # Settings
    notification_preferences: JSON
    language: str (DEFAULT 'en')
    timezone: str (DEFAULT 'UTC')
    
    # Relationships
    health_records: List[HealthRecord]
    reminders: List[Reminder]
    family_members: List[FamilyMember]
    emergency_contacts: List[EmergencyContact]
    chats: List[ChatMessage]
```

#### HealthRecord

```python
class HealthRecord:
    id: int (PK)
    user_id: int (FK, NOT NULL)
    mood: int (1-10, NOT NULL)
    energy: int (1-10, NOT NULL)
    sleep_quality: int (1-10, NOT NULL)
    symptoms: str (OPTIONAL)
    notes: str (OPTIONAL)
    
    # Optional vital signs
    blood_pressure_systolic: int (OPTIONAL)
    blood_pressure_diastolic: int (OPTIONAL)
    heart_rate: int (OPTIONAL)
    temperature: float (OPTIONAL)
    weight: float (OPTIONAL)
    
    created_at: datetime (DEFAULT now)
    updated_at: datetime (DEFAULT now)
```

#### Reminder

```python
class Reminder:
    id: int (PK)
    user_id: int (FK, NOT NULL)
    medication_name: str (NOT NULL)
    dosage: str (NOT NULL)
    frequency: enum ['daily', 'twice_daily', 'custom'] (NOT NULL)
    scheduled_times: JSON (list of times)
    is_active: bool (DEFAULT True)
    created_at: datetime (DEFAULT now)
    updated_at: datetime (DEFAULT now)
    
    # Tracking
    last_reminded: datetime (OPTIONAL)
    adherence_count: int (DEFAULT 0)
    total_count: int (DEFAULT 0)
```

#### ReminderConfirmation

```python
class ReminderConfirmation:
    id: int (PK)
    reminder_id: int (FK, NOT NULL)
    user_id: int (FK, NOT NULL)
    confirmed_at: datetime (NOT NULL)
    notes: str (OPTIONAL)
```

#### ChatMessage

```python
class ChatMessage:
    id: int (PK)
    user_id: int (FK, NOT NULL)
    sender: enum ['user', 'assistant'] (NOT NULL)
    message: str (NOT NULL)
    created_at: datetime (DEFAULT now)
    
    # Claude API tracking
    model_used: str (DEFAULT 'claude-3-5-sonnet-20241022')
    tokens_used: int (OPTIONAL)
```

#### FamilyMember

```python
class FamilyMember:
    id: int (PK)
    user_id: int (FK, NOT NULL)
    family_email: str (NOT NULL)
    relationship: str (son, daughter, spouse, friend, caregiver, etc.)
    can_view_health: bool (DEFAULT True)
    can_view_reminders: bool (DEFAULT False)
    can_message: bool (DEFAULT True)
    invitation_sent_at: datetime (OPTIONAL)
    accepted_at: datetime (OPTIONAL)
    created_at: datetime (DEFAULT now)
```

#### EmergencyContact

```python
class EmergencyContact:
    id: int (PK)
    user_id: int (FK, NOT NULL)
    name: str (NOT NULL)
    relationship: str (NOT NULL)
    phone: str (NOT NULL)
    email: str (OPTIONAL)
    is_primary: bool (DEFAULT False)
    notification_method: enum ['sms', 'email', 'both'] (DEFAULT 'both')
    created_at: datetime (DEFAULT now)
```

#### EmergencyAlert

```python
class EmergencyAlert:
    id: int (PK)
    user_id: int (FK, NOT NULL)
    triggered_at: datetime (DEFAULT now)
    user_location: str (OPTIONAL)
    status: enum ['triggered', 'acknowledged', 'resolved'] (DEFAULT 'triggered')
    responded_by: str (OPTIONAL)
    resolved_at: datetime (OPTIONAL)
```

### Data Storage

**PostgreSQL Tables**:
```sql
users (id, email, phone, first_name, last_name, ...)
health_records (id, user_id, mood, energy, sleep_quality, ...)
reminders (id, user_id, medication_name, frequency, ...)
reminder_confirmations (id, reminder_id, user_id, confirmed_at, ...)
chat_messages (id, user_id, sender, message, ...)
family_members (id, user_id, family_email, relationship, ...)
emergency_contacts (id, user_id, name, phone, ...)
emergency_alerts (id, user_id, triggered_at, ...)
sessions (id, user_id, token, expires_at, ...)
```

**Redis Keys**:
```
sessions:{token}           # User session (TTL: 30 min)
user_rates:{user_id}       # Rate limiting counter
cache:user:{user_id}       # Cached user profile (TTL: 1 hour)
cache:health:{user_id}     # Recent health data
cache:reminders:{user_id}  # Active reminders
```

---

## API Specifications

### Base URL

```
http://localhost:8000/api/v1
https://api.eldercareassistant.com/api/v1 (Production)
```

### Authentication

All endpoints require JWT token in header:
```
Authorization: Bearer {token}
```

Exceptions:
- POST /auth/register
- POST /auth/login
- GET /health (public)

### Authentication Endpoints

#### POST /auth/register

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-123-4567"
}
```

**Response** (201):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "message": "Registration successful. Please verify your email."
}
```

**Errors**:
- 400: Invalid email or weak password
- 409: Email already registered

#### POST /auth/login

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Errors**:
- 401: Invalid credentials
- 429: Too many login attempts

#### POST /auth/refresh

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Health Endpoints

#### GET /health/status

**Description**: Get current health status

**Response** (200):
```json
{
  "user_id": 1,
  "last_checkin": "2026-06-09T14:30:00Z",
  "mood": 7,
  "energy": 6,
  "sleep_quality": 8,
  "symptoms": [],
  "trend_7_days": "stable"
}
```

#### POST /health/checkin

**Request**:
```json
{
  "mood": 7,
  "energy": 6,
  "sleep_quality": 8,
  "symptoms": ["headache"],
  "notes": "Good day overall"
}
```

**Response** (201):
```json
{
  "id": 42,
  "user_id": 1,
  "mood": 7,
  "energy": 6,
  "sleep_quality": 8,
  "created_at": "2026-06-09T14:30:00Z"
}
```

#### GET /health/history

**Query Parameters**:
- days: 7, 30, 90 (default: 7)

**Response** (200):
```json
{
  "period": 7,
  "entries": [
    {
      "date": "2026-06-09",
      "mood": 7,
      "energy": 6,
      "sleep_quality": 8
    },
    ...
  ],
  "trends": {
    "mood_trend": "stable",
    "energy_trend": "declining",
    "sleep_trend": "improving"
  }
}
```

### Reminder Endpoints

#### GET /reminders

**Response** (200):
```json
{
  "active": [
    {
      "id": 1,
      "medication_name": "Blood Pressure Med",
      "dosage": "10mg",
      "frequency": "daily",
      "scheduled_times": ["08:00"],
      "next_reminder": "2026-06-09T08:00:00Z"
    }
  ],
  "inactive": []
}
```

#### POST /reminders

**Request**:
```json
{
  "medication_name": "Blood Pressure Med",
  "dosage": "10mg",
  "frequency": "daily",
  "scheduled_times": ["08:00"],
  "notification_methods": ["app", "email"]
}
```

**Response** (201):
```json
{
  "id": 1,
  "medication_name": "Blood Pressure Med",
  "created_at": "2026-06-09T10:00:00Z"
}
```

#### PUT /reminders/{id}

**Request**: Same as POST

**Response** (200): Updated reminder object

#### DELETE /reminders/{id}

**Response** (204): No content

### Chat Endpoints

#### POST /chat

**Request**:
```json
{
  "message": "I have a headache, what should I do?"
}
```

**Response** (200):
```json
{
  "id": 1,
  "message": "I have a headache, what should I do?",
  "response": "I'm sorry to hear you have a headache. Here are some general suggestions:\n\n1. Rest in a quiet, dark room\n2. Stay hydrated...",
  "created_at": "2026-06-09T14:30:00Z"
}
```

#### GET /chat/history

**Query Parameters**:
- limit: 50 (default: 50, max: 100)
- offset: 0 (default: 0)

**Response** (200):
```json
{
  "total": 150,
  "messages": [
    {
      "id": 150,
      "sender": "user",
      "message": "Good morning",
      "created_at": "2026-06-09T09:00:00Z"
    },
    {
      "id": 149,
      "sender": "assistant",
      "message": "Good morning! How are you feeling today?",
      "created_at": "2026-06-09T09:00:30Z"
    }
  ]
}
```

### Family Endpoints

#### POST /family/members

**Request**:
```json
{
  "family_email": "daughter@example.com",
  "relationship": "daughter",
  "can_view_health": true,
  "can_view_reminders": false,
  "can_message": true
}
```

**Response** (201):
```json
{
  "id": 1,
  "family_email": "daughter@example.com",
  "status": "invitation_sent",
  "invitation_sent_at": "2026-06-09T10:00:00Z"
}
```

#### GET /family/members

**Response** (200):
```json
{
  "members": [
    {
      "id": 1,
      "name": "Jane Doe",
      "relationship": "daughter",
      "status": "accepted",
      "can_view_health": true,
      "can_view_reminders": false
    }
  ]
}
```

#### DELETE /family/members/{id}

**Response** (204): No content

### Emergency Endpoints

#### POST /emergency/alert

**Request**:
```json
{
  "location": "Home",
  "urgency": "high"
}
```

**Response** (201):
```json
{
  "alert_id": 42,
  "status": "triggered",
  "contacts_notified": 3,
  "created_at": "2026-06-09T14:30:00Z"
}
```

#### GET /emergency/contacts

**Response** (200):
```json
{
  "contacts": [
    {
      "id": 1,
      "name": "Jane Doe",
      "relationship": "daughter",
      "phone": "+1-555-123-4567",
      "is_primary": true
    }
  ]
}
```

#### POST /emergency/contacts

**Request**:
```json
{
  "name": "Jane Doe",
  "relationship": "daughter",
  "phone": "+1-555-123-4567",
  "is_primary": false
}
```

**Response** (201): Created contact object

### Response Format

All responses follow this structure:

**Success**:
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2026-06-09T14:30:00Z"
}
```

**Error**:
```json
{
  "status": "error",
  "error": "Invalid input",
  "code": "VALIDATION_ERROR",
  "details": {
    "field": "message",
    "issue": "message cannot be empty"
  },
  "timestamp": "2026-06-09T14:30:00Z"
}
```

### Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Successful GET/PUT |
| 201 | Created - Successful POST |
| 204 | No Content - Successful DELETE |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 429 | Too Many Requests - Rate limited |
| 500 | Internal Server Error |

### Pagination

For list endpoints:
```
GET /endpoint?limit=20&offset=0
```

Response:
```json
{
  "total": 150,
  "limit": 20,
  "offset": 0,
  "items": [ ... ]
}
```

---

## Security Specifications

### Authentication & Authorization

**JWT Token Structure**:
```
Header: {
  "alg": "HS256",
  "typ": "JWT"
}

Payload: {
  "sub": "1",              // User ID
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234569690,       // 30 minutes
  "iss": "elder-care-assistant"
}

Signature: HMAC-SHA256
```

**Token Expiration**:
- Access token: 30 minutes
- Refresh token: 7 days
- Session timeout: 1 hour inactivity

**Password Requirements**:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

### Data Security

**Encryption**:
- Data in transit: TLS 1.3+
- Data at rest: AES-256 for sensitive fields
  - Health records
  - Chat messages
  - Emergency contact info

**Sensitive Fields**:
- Passwords: Hashed with bcrypt (cost: 12)
- Tokens: Stored in Redis with expiration
- API Keys: Never logged or displayed
- PII: Encrypted in database

### Rate Limiting

**Endpoint Limits**:
```
POST /auth/login:              5 attempts/15 min
POST /auth/register:           10 attempts/hour
POST /chat:                    30 messages/hour
POST /health/checkin:          5 check-ins/day
POST /emergency/alert:         Unlimited (emergency)
GET * (general):               100 requests/minute
```

**Backoff Strategy**:
- 1st failure: 1 second delay
- 2nd failure: 2 second delay
- 3rd failure: 4 second delay
- 4th failure: 8 second delay
- 5th failure: 15 minute lockout

### CORS Policy

**Allowed Origins** (Development):
```
http://localhost:3000
http://localhost:3001
http://localhost:5173
http://127.0.0.1:3000
```

**Allowed Origins** (Production):
```
https://eldercareassistant.com
https://www.eldercareassistant.com
```

**Methods**: GET, POST, PUT, DELETE, OPTIONS

**Headers**: Content-Type, Authorization, Accept

### HIPAA Compliance

**Requirements**:
- Audit logging for all health data access
- Data retention: Keep for 6 years minimum
- Data deletion: Secure wipe (DOD 5220.22-M)
- Breach notification: Within 24 hours
- Encryption: All PII encrypted
- Access control: Role-based access
- Business Associate Agreements (BAAs) for third parties

**Audit Log Fields**:
```json
{
  "timestamp": "2026-06-09T14:30:00Z",
  "user_id": 1,
  "action": "read_health_record",
  "resource_id": 42,
  "ip_address": "192.168.1.1",
  "status": "success"
}
```

### GDPR Compliance

**User Rights**:
- Right to access: Data export in JSON/CSV
- Right to deletion: Soft delete then permanent after 90 days
- Right to correction: Can update own data
- Right to portability: Export in machine-readable format

**Data Processing**:
- Consent before processing
- Minimize data collection
- Transparency in data use
- Data retention limits

### API Security

**Best Practices**:
- Validate all input
- Sanitize output
- No SQL injection (use parameterized queries)
- No XSS (context-aware encoding)
- CSRF protection: Use same-site cookies
- Security headers: HSTS, X-Content-Type-Options, CSP

**Security Headers**:
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

---

## Performance Requirements

### Response Time Targets

| Endpoint | Target | P95 |
|----------|--------|-----|
| GET endpoints | <200ms | <500ms |
| POST endpoints | <500ms | <1000ms |
| Chat (Claude API) | <3s | <5s |
| Health history | <300ms | <1000ms |

### Throughput

- Handle 1000 concurrent users
- Support 100 requests/second
- Database: 1000 queries/second

### Resource Usage

**CPU**: Max 80% under normal load
**Memory**: Max 4GB per instance
**Database Connections**: Max 100 connections

### Caching Strategy

**Redis Cache**:
- User profile: 1 hour TTL
- Health data: 30 minutes TTL
- Reminder list: 15 minutes TTL
- Chat history: 5 minutes TTL

**HTTP Caching**:
- GET requests: Cache-Control: max-age=300
- Health history: Cache-Control: max-age=600

### Database Indexing

**Critical Indexes**:
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_health_user_date ON health_records(user_id, created_at DESC);
CREATE INDEX idx_reminders_user ON reminders(user_id);
CREATE INDEX idx_chat_user_date ON chat_messages(user_id, created_at DESC);
CREATE INDEX idx_family_user ON family_members(user_id);
CREATE INDEX idx_emergency_contacts_user ON emergency_contacts(user_id);
```

---

## Deployment Specifications

### Environment Variables

```env
# Application
ENV=production
DEBUG=False
SECRET_KEY=<random-64-char-string>
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:password@host:5432/db
DATABASE_ECHO=False

# Redis
REDIS_URL=redis://host:6379/0

# JWT
JWT_SECRET=<random-64-char-string>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=0.5
JWT_REFRESH_EXPIRATION_DAYS=7

# Claude API
CLAUDE_API_KEY=<anthropic-api-key>
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# CORS
CORS_ORIGINS=https://eldercareassistant.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<email>
SMTP_PASSWORD=<password>
SENDER_EMAIL=noreply@eldercareassistant.com

# SMS (Optional)
TWILIO_ACCOUNT_SID=<account-sid>
TWILIO_AUTH_TOKEN=<auth-token>
TWILIO_PHONE_NUMBER=<phone>
```

### Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/elder_care
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      - db
      - cache

  db:
    image: postgres:12
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: elder_care
    volumes:
      - postgres_data:/var/lib/postgresql/data

  cache:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Production Checklist

- [ ] All environment variables configured
- [ ] Database backups enabled
- [ ] SSL certificates installed
- [ ] Email/SMS credentials verified
- [ ] Logging configured (ELK stack)
- [ ] Monitoring enabled (Prometheus/Grafana)
- [ ] Security headers configured
- [ ] Rate limiting tested
- [ ] CORS origins restricted
- [ ] Database encrypted
- [ ] API keys rotated
- [ ] Backup/recovery tested
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated

---

## Testing Specifications

### Test Coverage Requirements

- Minimum 80% overall coverage
- 100% coverage for auth endpoints
- 100% coverage for emergency endpoints
- 90% coverage for health data endpoints
- 85% coverage for chat endpoints

### Test Types

**Unit Tests**:
```python
def test_user_registration_success():
    # Arrange
    user_data = {...}
    
    # Act
    result = register_user(user_data)
    
    # Assert
    assert result.id is not None
    assert result.email == user_data['email']
```

**Integration Tests**:
```python
def test_health_checkin_flow():
    # Register user
    # Login
    # Submit health check-in
    # Verify in database
    # Verify family notification sent
```

**API Tests**:
```python
def test_get_health_status_api():
    # Make request to GET /health/status
    # Verify response code: 200
    # Verify response schema
    # Verify data accuracy
```

**Security Tests**:
- SQL injection attempts
- XSS payload injection
- Authentication bypass
- Authorization checks
- Rate limiting

**Performance Tests**:
```python
def test_health_history_performance():
    # Load 1000 health records
    # Time GET /health/history
    # Assert response time < 500ms
```

### Testing Tools

- Framework: pytest
- Fixtures: pytest-fixtures
- Mocking: unittest.mock, responses
- Coverage: pytest-cov
- Performance: pytest-benchmark
- Database: pytest-postgresql (real PostgreSQL)

---

## Compliance Requirements

### HIPAA (US)

**Privacy Rule**:
- Minimum necessary principle
- Disclosure accounting
- Patient rights (access, amendment, deletion)
- Breach notification (60 days)

**Security Rule**:
- Administrative safeguards
- Physical safeguards
- Technical safeguards
- Organizational policies

**Breach Notification**:
- Notify patients within 60 days
- Notify HHS
- Notify media (if >500 affected)
- Document breach

### GDPR (EU)

**Data Subject Rights**:
- Right to access personal data
- Right to be forgotten
- Right to data portability
- Right to object

**Data Protection**:
- Data minimization
- Purpose limitation
- Storage limitation
- Integrity and confidentiality

**Data Protection Impact Assessment (DPIA)**: Required before deployment

### CCPA (California)

**Consumer Rights**:
- Know what personal data is collected
- Delete personal data
- Opt-out of sale
- Non-discrimination for exercising rights

### Regional Compliance

**Canada (PIPEDA)**:
- Consent before collection
- Accuracy and retention requirements
- Secure disposal

**Australia (Privacy Act)**:
- Privacy principles
- Notifiable data breaches

---

## Appendices

### A. API Error Codes

| Code | HTTP | Meaning |
|------|------|---------|
| VALIDATION_ERROR | 400 | Input validation failed |
| UNAUTHORIZED | 401 | No/invalid authentication |
| FORBIDDEN | 403 | No permission |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource already exists |
| RATE_LIMITED | 429 | Too many requests |
| INVALID_TOKEN | 401 | Token expired/invalid |
| ACCOUNT_LOCKED | 403 | Account temporarily locked |

### B. Configuration Templates

See `.env.example` for all template configurations.

### C. Deployment Runbook

See ops documentation for deployment procedures.

### D. Glossary

- **PII**: Personally Identifiable Information
- **JWT**: JSON Web Token
- **CORS**: Cross-Origin Resource Sharing
- **TTL**: Time To Live
- **API**: Application Programming Interface
- **ORM**: Object-Relational Mapping
- **SDK**: Software Development Kit

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-09 | Initial specification |

## Document Control

- **Owner**: Development Team
- **Last Reviewed**: 2026-06-09
- **Next Review**: 2026-09-09
- **Status**: Active

---

**End of Specification Document**

For questions or clarifications, contact: dev-team@eldercareassistant.com
