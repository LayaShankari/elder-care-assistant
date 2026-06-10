from app.config import settings


def test_default_app_settings_are_available():
    assert settings.APP_NAME == "Elder Care Assistant"
    assert settings.JWT_ALGORITHM == "HS256"
    assert settings.RATE_LIMIT_REQUESTS > 0
