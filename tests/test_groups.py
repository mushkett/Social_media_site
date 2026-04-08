from django.urls import reverse

import pytest

from groups.models import Group, GroupMember


@pytest.fixture
def group(db):
    """Create a test group."""
    return Group.objects.create(name='Test Group', description='A test group description')


class TestGroupModel:
    def test_group_str(self, group):
        assert str(group) == 'Test Group'

    def test_group_slug_auto_generated(self, group):
        assert group.slug == 'test-group'

    def test_group_absolute_url(self, group):
        assert group.get_absolute_url() == f'/groups/posts/in/{group.slug}'


class TestGroupMemberModel:
    def test_group_member_str(self, user, group):
        membership = GroupMember.objects.create(user=user, group=group)
        assert str(membership) == user.username

    def test_unique_membership(self, user, group):
        from django.db import IntegrityError

        GroupMember.objects.create(user=user, group=group)
        with pytest.raises(IntegrityError):
            GroupMember.objects.create(user=user, group=group)


class TestGroupViews:
    def test_group_list_view(self, client, group):
        response = client.get(reverse('groups:all'))
        assert response.status_code == 200
        assert 'Test Group' in response.content.decode()

    def test_group_detail_view(self, client, group):
        response = client.get(reverse('groups:single', kwargs={'slug': group.slug}))
        assert response.status_code == 200

    def test_create_group_requires_login(self, client):
        response = client.get(reverse('groups:create'))
        assert response.status_code == 302  # Redirect to login

    def test_create_group_authenticated(self, authenticated_client):
        response = authenticated_client.get(reverse('groups:create'))
        assert response.status_code == 200

    def test_join_group(self, authenticated_client, user, group):
        response = authenticated_client.post(reverse('groups:join', kwargs={'slug': group.slug}))
        assert response.status_code == 302
        assert GroupMember.objects.filter(user=user, group=group).exists()

    def test_leave_group(self, authenticated_client, user, group):
        GroupMember.objects.create(user=user, group=group)
        response = authenticated_client.post(reverse('groups:leave', kwargs={'slug': group.slug}))
        assert response.status_code == 302
        assert not GroupMember.objects.filter(user=user, group=group).exists()
