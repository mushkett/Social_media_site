"""Post model with markdown support."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.utils import render_markdown
from groups.models import Group

if TYPE_CHECKING:
    from accounts.models import User as UserType

User = get_user_model()


class Post(models.Model):
    """User post with optional group association."""

    user: models.ForeignKey[UserType] = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False, blank=True)
    group: models.ForeignKey[Group | None] = models.ForeignKey(
        Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.message[:50]

    def save(self, *args, **kwargs) -> None:
        self.message_html = render_markdown(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        # pylint: disable=no-member
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['group', '-created_at']),
        ]
        constraints = [models.UniqueConstraint(fields=['user', 'message'], name='unique_user_message')]
