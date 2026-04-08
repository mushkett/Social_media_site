"""
Custom User model for the Social Media application.

Django Best Practice: Always use a custom User model from the start,
even if you don't need extra fields yet. This makes future extensions
much easier without complex migrations.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Currently identical to the default User, but allows for easy
    extension in the future without migration headaches.
    """

    class Meta:
        db_table = 'auth_user'  # Keep same table name for compatibility
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self) -> str:
        return self.username
