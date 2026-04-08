from django.urls import reverse

import pytest

from groups.models import Group
from posts.models import Post


@pytest.fixture
def post(db, user):
    """Create a test post."""
    return Post.objects.create(user=user, message='Test post message')


@pytest.fixture
def group(db):
    """Create a test group."""
    return Group.objects.create(name='Test Group', description='A test group')


class TestPostModel:
    def test_post_str(self, post):
        assert str(post) == 'Test post message'

    def test_post_html_generated(self, post):
        assert post.message_html is not None
        assert len(post.message_html) > 0

    def test_post_ordering(self, user, db):
        post1 = Post.objects.create(user=user, message='First')
        post2 = Post.objects.create(user=user, message='Second')
        posts = list(Post.objects.all())
        # Most recent first
        assert posts[0] == post2
        assert posts[1] == post1


class TestPostViews:
    def test_post_list_view(self, client, post):
        response = client.get(reverse('posts:all'))
        assert response.status_code == 200

    def test_create_post_requires_login(self, client):
        response = client.get(reverse('posts:create'))
        assert response.status_code == 302

    def test_create_post_authenticated(self, authenticated_client):
        response = authenticated_client.get(reverse('posts:create'))
        assert response.status_code == 200

    def test_user_posts_view(self, client, user, post):
        response = client.get(reverse('posts:for_user', kwargs={'username': user.username}))
        assert response.status_code == 200

    def test_delete_own_post(self, authenticated_client, user, post):
        response = authenticated_client.post(reverse('posts:delete', kwargs={'pk': post.pk}))
        assert response.status_code == 302
        assert not Post.objects.filter(pk=post.pk).exists()
