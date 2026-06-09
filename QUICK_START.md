# Elder Care Assistant - Quick Reference 📖

## Project Structure

```
elder-care-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Configuration management
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── health.py          # Health monitoring endpoints
│   │   │   ├── reminders.py       # Reminder management endpoints
│   │   │   ├── chat.py            # Chat/companion endpoints
│   │   │   ├── family.py          # Family coordination endpoints
│   │   │   └── emergency.py       # Emergency endpoints
│   ├── agents/
│   │   ├── base.py                # Base agent class
│   │   ├── health_monitor.py      # Health monitoring agent
│   │   ├── companion.py           # Companion/chat agent
│   │   ├── activity_reminder.py   # Reminder agent (TODO)
│   │   ├── emergency_handler.py   # Emergency agent (TODO)
│   │   └── family_coordinator.py  # Family agent (TODO)
│   ├── database/
│   │   ├── db.py                  # Database connection
│   │   └── base.py                # SQLAlchemy base
│   ├── models/
│   │   └── models.py              # Database models
│   ├── schemas/
│   │   └── schemas.py             # Pydantic schemas
│   ├── services/
│   │   └── services.py            # Business logic services
│   ├── middleware/
│   │   ├── auth.py                # Authentication middleware
│   │   └── error_handler.py       # Error handling middleware
│   ├── tasks/
│   │   └── celery.py              # Celery background tasks
│   └── utils/
│       └── security.py            # JWT, hashing utilities
├── tests/                         # Test files (TODO)
├── docs/                          # Additional documentation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .env                           # Actual environment (git ignored)
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Docker compose configuration
├── Dockerfile                     # Docker image definition
├── start.sh                       # Quick start script
├── README.md                      # Project overview
├── CONTRIBUTING.md                # Contributing guidelines
├── USER_MANUAL.md                 # User documentation
├── SPEC.md                        # Technical specification
└── SPEC_KIT.md                    # Comprehensive spec kit
```

## Running the Application

### Option 1: Local Development

```bash
# 1. Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup .env
cp .env.example .env

# 4. Start Redis
redis-server

# 5. Start Celery (in another terminal)
celery -A app.tasks.celery worker --loglevel=info

# 6. Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker Compose

```bash
docker-compose up
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token

### Health Monitoring
- `POST /api/v1/health/readings` - Add health reading
- `GET /api/v1/health/readings` - Get reading history
- `GET /api/v1/health/summary` - Get health summary

### Reminders
- `POST /api/v1/reminders` - Create reminder
- `GET /api/v1/reminders` - List reminders
- `GET /api/v1/reminders/upcoming` - Get upcoming reminders
- `PATCH /api/v1/reminders/{id}/complete` - Mark complete
- `DELETE /api/v1/reminders/{id}` - Delete reminder

### Chat
- `POST /api/v1/chat/message` - Send message to companion
- `GET /api/v1/chat/history` - Get chat history

### Family
- `POST /api/v1/family/members` - Add family member
- `GET /api/v1/family/members` - List family members
- `DELETE /api/v1/family/members/{id}` - Remove family member
- `GET /api/v1/family/dashboard` - Get family dashboard
- `POST /api/v1/family/summary` - Send daily summary

### Emergency
- `POST /api/v1/emergency/activate` - Activate emergency protocol
- `GET /api/v1/emergency/status/{id}` - Get emergency status
- `POST /api/v1/emergency/contacts` - Add emergency contact
- `GET /api/v1/emergency/history` - Get emergency history

## Database Models

- **User** - User accounts with preferences
- **HealthReading** - Health metrics (BP, glucose, temp, etc)
- **Reminder** - Medication, meal, appointment reminders
- **NormalRange** - User-specific health ranges
- **FamilyMember** - Family members with permissions
- **ChatMessage** - Conversation history

## Agents

### Health Monitor Agent
- Analyzes health readings
- Detects anomalies
- Provides recommendations
- Alerts family if needed

### Companion Agent
- Conversational support
- Feature explanations
- Emotional support
- General information

### (TODO) Remaining Agents
- Activity Reminder Agent - Manages reminders
- Emergency Handler Agent - Handles emergencies
- Family Coordinator Agent - Manages family communication

## Configuration

All configuration is in `app/config.py` and read from `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost/db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret-key
CLAUDE_API_KEY=your-claude-key
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/unit/test_health_service.py -v
```

## Key Technologies

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **AI**: Claude API (Anthropic)
- **ORM**: SQLAlchemy
- **Auth**: JWT
- **Validation**: Pydantic

## Development Tips

1. **Run with auto-reload**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access API docs**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Check database**:
   ```bash
   psql -U elder_user -d elder_care_db
   ```

4. **Monitor Celery**:
   ```bash
   celery -A app.tasks.celery flower  # Open http://localhost:5555
   ```

5. **View logs**:
   ```bash
   tail -f app.log
   ```

## Common Issues

**PostgreSQL connection error**
```bash
# Ensure PostgreSQL is running
psql postgres

# Check credentials in .env
```

**Redis connection error**
```bash
# Start Redis
redis-server
```

**Port already in use**
```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Setup database: PostgreSQL running
3. ✅ Configure `.env` with your keys
4. ✅ Start Redis: `redis-server`
5. ✅ Run migrations: `alembic upgrade head`
6. ✅ Start API: `uvicorn app.main:app --reload`
7. 📝 Implement missing agents
8. 📝 Add comprehensive tests
9. 📝 Frontend integration

## Support

- **API Docs**: http://localhost:8000/docs
- **Issues**: Check GitHub issues
- **Docs**: See SPEC_KIT.md, README.md
- **Contributing**: See CONTRIBUTING.md

---

**Version**: 1.0 | **Status**: Hackathon MVP | **Last Updated**: 2026-06-09
