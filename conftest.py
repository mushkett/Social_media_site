import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(autouse=True)
def disable_ratelimit(settings):
    """Disable rate limiting for all tests."""
    settings.RATELIMIT_ENABLE = False


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def authenticated_client(client, user):
    """Return a client logged in as user."""
    client.force_login(user)
    return client
