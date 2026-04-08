"""Group models with markdown support."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.utils import render_markdown

if TYPE_CHECKING:
    from accounts.models import User as UserType

User = get_user_model()


class Group(models.Model):
    """A group that users can join and post to."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members: models.ManyToManyField = models.ManyToManyField(User, through='GroupMember')
    creator: models.ForeignKey[UserType | None] = models.ForeignKey(
        User,
        related_name='created_groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name, allow_unicode=True)
        self.description_html = render_markdown(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]


class GroupMember(models.Model):
    """Through model for User-Group M2M relationship."""

    group: models.ForeignKey[Group] = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user: models.ForeignKey[UserType] = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        # pylint: disable=no-member
        return self.user.username

    class Meta:
        indexes = [
            models.Index(fields=['group', 'user']),
            models.Index(fields=['-joined_at']),
        ]
        constraints = [models.UniqueConstraint(fields=['group', 'user'], name='unique_group_member')]
