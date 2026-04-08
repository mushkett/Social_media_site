from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestSignUp:
    def test_signup_page_loads(self, client):
        response = client.get(reverse('accounts:signup'))
        assert response.status_code == 200

    def test_signup_creates_user(self, client, db):
        response = client.post(
            reverse('accounts:signup'),
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'complexpass123!',
                'password2': 'complexpass123!',
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()


class TestLogin:
    def test_login_page_loads(self, client):
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200

    def test_login_valid_credentials(self, client, user):
        response = client.post(
            reverse('accounts:login'),
            {'username': 'testuser', 'password': 'testpass123'},
        )
        assert response.status_code == 302

    def test_login_invalid_credentials(self, client, user):
        response = client.post(
            reverse('accounts:login'),
            {'username': 'testuser', 'password': 'wrongpass'},
        )
        assert response.status_code == 200  # Stay on login page


class TestLogout:
    def test_logout(self, authenticated_client):
        response = authenticated_client.post(reverse('accounts:logout'))
        assert response.status_code == 302
