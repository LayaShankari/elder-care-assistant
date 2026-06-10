# Elder Care Assistant

An AI-powered health monitoring and companion system designed to provide personalized care support for elderly individuals and their families.

## Overview

Elder Care Assistant is a comprehensive platform that combines AI-driven chatbot capabilities with health monitoring, medication reminders, and family communication tools. Built with modern web technologies, it enables caregivers and families to stay connected and informed about the well-being of their elderly loved ones.

## Key Features

- **AI-Powered Chat Companion**: Conversational AI using Claude to provide emotional support and answer health-related questions
- **Health Monitoring**: Track vital signs and health metrics with periodic check-ins
- **Medication Reminders**: Automated reminders for medications and health appointments
- **Family Connectivity**: Secure channels for family members to stay updated and communicate
- **Emergency Response**: Quick access to emergency contacts and alert systems
- **Secure Authentication**: JWT-based authentication with optional 2FA support
- **Multi-device Support**: Responsive design supporting desktop, tablet, and mobile devices

## Tech Stack

**Backend**
- FastAPI (Python web framework)
- PostgreSQL (Primary database)
- Redis (Caching and session management)
- Claude API (AI chat functionality)
- SQLAlchemy (ORM)
- Pydantic (Data validation)

**Frontend** *(Optional - configure in frontend repo)*
- React or similar framework
- CORS-enabled for API access

## Project Structure

```
elder-care-assistant/
├── app/
│   ├── main.py                 # FastAPI application setup
│   ├── config.py               # Configuration management
│   ├── api/
│   │   └── routes/             # API endpoints (auth, health, reminders, chat, family, emergency)
│   ├── models/                 # Database models
│   ├── schemas/                # Pydantic schemas for validation
│   ├── database/               # Database configuration
│   ├── services/               # Business logic
│   ├── middleware/             # Authentication, error handling
│   └── utils/                  # Helper utilities
├── tests/                      # Test suite
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Claude API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/elder-care-assistant.git
   cd elder-care-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up the database**
   ```bash
   alembic upgrade head  # If using migrations
   ```

6. **Start the server**
   ```bash
   python -m app.main
   # Or with reload:
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Key environment variables to configure:

```env
ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/elder_care_db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-jwt-secret-change-in-production
CLAUDE_API_KEY=your-claude-api-key
```

See `.env.example` for all available options.

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Health
- `GET /api/v1/health/status` - Get health status
- `POST /api/v1/health/checkin` - Submit health check-in

### Reminders
- `GET /api/v1/reminders` - List reminders
- `POST /api/v1/reminders` - Create reminder
- `PUT /api/v1/reminders/{id}` - Update reminder
- `DELETE /api/v1/reminders/{id}` - Delete reminder

### Chat
- `POST /api/v1/chat` - Send chat message
- `GET /api/v1/chat/history` - Get chat history

### Family
- `GET /api/v1/family/members` - List family members
- `POST /api/v1/family/members` - Add family member
- `POST /api/v1/family/notifications` - Send notification

### Emergency
- `POST /api/v1/emergency/alert` - Trigger emergency alert
- `GET /api/v1/emergency/contacts` - Get emergency contacts

## Security Considerations

- All sensitive data is environment-based and never committed
- JWT tokens expire after 30 minutes with 7-day refresh window
- CORS is configured for trusted origins only
- SQL injection prevention through parameterized queries (SQLAlchemy)
- Rate limiting enabled (100 requests/60 seconds)
- HTTPS recommended for production

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Deployment

### Production Checklist

- [ ] Change all default secrets in `.env`
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure production database (PostgreSQL)
- [ ] Set up Redis for caching
- [ ] Configure email/SMS credentials (optional)
- [ ] Enable security headers
- [ ] Set up monitoring and logging
- [ ] Configure backups

### Docker Deployment

*Optional: Create Dockerfile and docker-compose.yml*

```bash
docker-compose up -d
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## User Manual

See [USER_MANUAL.md](USER_MANUAL.md) for end-user documentation and usage instructions.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For support, please:
1. Check the [USER_MANUAL.md](USER_MANUAL.md)
2. Review open issues on GitHub
3. Create a new issue with detailed information

## Authors

- Developed for elderly care support and family connectivity

## Acknowledgments

- Built with FastAPI, PostgreSQL, and Claude AI
- Inspired by modern telehealth and elder care platforms
