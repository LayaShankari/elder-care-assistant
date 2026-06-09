# Contributing to Elder Care Assistant

Thank you for your interest in contributing to Elder Care Assistant! We welcome contributions from the community and are grateful for your involvement.

## Code of Conduct

This project is dedicated to providing a welcoming and inclusive environment for all contributors. We ask that you:
- Treat all people with respect and kindness
- Be open to constructive feedback
- Focus on what's best for the community
- Show empathy toward others

## Ways to Contribute

### Reporting Bugs

Found a bug? Please create an issue with:
1. **Clear description** of the bug
2. **Steps to reproduce** the issue
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots or logs** if applicable

Example:
```
Title: Chat endpoint returns 500 on special characters

Description:
When sending a message with certain special characters (é, ñ, 中文), 
the API returns a 500 Internal Server Error.

Steps to Reproduce:
1. Login to the application
2. Send a chat message: "Hello with é accent"
3. Observe error response

Expected: Message should be processed correctly
Actual: 500 error returned
```

### Suggesting Features

Have an idea? We'd love to hear it! Please create a feature request with:
1. **Clear title** describing the feature
2. **Detailed description** of what you want
3. **Why** this would be valuable
4. **Proposed implementation** (optional)

Example:
```
Title: Add voice-to-text for medication reminders

Description:
Allow users to confirm medication reminders using voice commands 
for accessibility.

Benefit: Improves accessibility for users with mobility challenges
```

### Submitting Code Changes

#### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/elder-care-assistant.git
   cd elder-care-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/bug-description
   ```

#### Development Guidelines

**Code Style**
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use type hints for all functions

**Example:**
```python
from typing import Optional, List
from fastapi import HTTPException

async def get_user_reminders(
    user_id: int,
    skip: int = 0,
    limit: int = 10
) -> List[Reminder]:
    """Fetch paginated reminders for a user."""
    reminders = db.query(Reminder).filter(
        Reminder.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminders found")
    
    return reminders
```

**Naming Conventions**
- Classes: `PascalCase` (e.g., `UserModel`, `HealthService`)
- Functions: `snake_case` (e.g., `get_user_health_status`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- Private members: prefix with `_` (e.g., `_internal_helper`)

**Comments and Documentation**
- Use docstrings for all public functions and classes
- Write comments only for non-obvious logic
- Keep comments concise and accurate

```python
def calculate_medication_schedule(
    medication: Medication
) -> List[datetime]:
    """Calculate next medication reminders based on frequency.
    
    Args:
        medication: The medication object with frequency settings
        
    Returns:
        List of datetime objects for upcoming reminders
    """
    # Implementation here
```

#### Making Changes

1. **Make your changes** following the guidelines above
2. **Run tests** to ensure nothing breaks
   ```bash
   pytest
   pytest --cov=app  # Check coverage
   ```

3. **Format code** using black (if configured)
   ```bash
   black .
   ```

4. **Run linting** checks
   ```bash
   pylint app/
   flake8 app/
   ```

5. **Commit your changes** with clear messages
   ```bash
   git add .
   git commit -m "Add feature: voice confirmation for reminders"
   ```

   Commit message guidelines:
   - Start with a verb: Add, Fix, Update, Remove, Refactor
   - Keep first line under 50 characters
   - Add detailed description if needed

   Examples:
   ```
   Add voice confirmation for medication reminders
   
   Implement voice-to-text functionality allowing users to 
   confirm medication reminders via voice commands. Uses 
   Web Speech API for browser-based transcription.
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Submitting a Pull Request

1. **Create a PR** with a descriptive title and description
2. **Link to issues** if applicable: "Fixes #123"
3. **Describe changes**:
   - What changed and why
   - How to test the changes
   - Any breaking changes
   - Screenshots/demos if UI changes

PR Template:
```markdown
## Description
Brief description of what this PR does.

Fixes #(issue number)

## Changes Made
- Change 1
- Change 2

## Testing
How to test these changes:
1. Step 1
2. Step 2

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Tested locally
```

#### PR Review Process

1. **Automated checks** must pass:
   - Tests
   - Linting
   - Code coverage

2. **Code review**:
   - At least one approval required
   - Constructive feedback will be provided
   - Be open to suggestions

3. **Merge**:
   - After approval and tests pass
   - Squash commits if preferred
   - Delete branch after merge

### Improving Documentation

Documentation improvements are always welcome! You can:
- Fix typos or clarify explanations
- Add examples or use cases
- Update outdated information
- Translate to other languages

## Project Structure Reference

Key files and directories:

```
app/
├── api/routes/          # API endpoint definitions
├── models/              # SQLAlchemy database models
├── schemas/             # Pydantic validation schemas
├── services/            # Business logic layer
├── middleware/          # Request/response middleware
└── utils/               # Shared utility functions

tests/                   # Test files (mirror app structure)
requirements.txt         # Project dependencies
requirements-dev.txt     # Development-only dependencies
```

## Commit Message Guidelines

Format your commits with:
1. **Type**: Add, Fix, Update, Refactor, Remove, Docs
2. **Scope**: Optional - which part (auth, health, chat)
3. **Description**: Clear, imperative mood

Examples:
```
Add voice confirmation for medication reminders
Fix null pointer in health check endpoint
Update database schema documentation
Refactor chat service for better error handling
Remove deprecated authentication method
Docs: Add API endpoint examples
```

## Testing

- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **Aim for >80% code coverage**

Example test:
```python
import pytest
from app.services.auth import authenticate_user
from app.schemas import UserLogin

def test_authenticate_user_success():
    """Test successful user authentication."""
    credentials = UserLogin(email="user@example.com", password="secure123")
    user = authenticate_user(credentials)
    assert user is not None
    assert user.email == "user@example.com"

def test_authenticate_user_invalid_password():
    """Test authentication with invalid password."""
    credentials = UserLogin(email="user@example.com", password="wrong")
    with pytest.raises(HTTPException):
        authenticate_user(credentials)
```

## Security Considerations

- Never commit secrets (API keys, passwords, tokens)
- Use environment variables for sensitive data
- Sanitize user input to prevent injection attacks
- Follow OWASP security guidelines
- Report security issues privately (don't create public issues)

## Performance Considerations

- Use database indexes for frequently queried fields
- Implement caching where appropriate (Redis)
- Optimize query performance
- Consider pagination for large datasets
- Monitor API response times

## Questions?

- Check existing issues for answers
- Review documentation in README.md
- Start a discussion if you're unsure

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Project release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for making Elder Care Assistant better!
