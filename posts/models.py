from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka
import bleach

from groups.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

# Allowed HTML tags for sanitized markdown output
ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
    'li', 'ol', 'p', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'br', 'hr', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'alt', 'title'],
}


class Post(models.Model):
    """User post with optional group association."""
    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Fixed: was auto_now
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False, blank=True)
    group = models.ForeignKey(
        Group,
        related_name='posts',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message[:50]

    def save(self, *args, **kwargs):  # Fixed: was *kwargs
        # Convert markdown to HTML and sanitize
        raw_html = misaka.html(self.message)
        self.message_html = bleach.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'message'],
                name='unique_user_message'
            )
        ]
