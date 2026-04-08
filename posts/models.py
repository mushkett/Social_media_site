from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

import nh3
from markdown_it import MarkdownIt

from groups.models import Group

User = get_user_model()

_md = MarkdownIt()

# Allowed HTML tags for sanitized markdown output
ALLOWED_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i',
    'li', 'ol', 'p', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'br', 'hr', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
}
ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title'},
    'abbr': {'title'},
    'img': {'src', 'alt', 'title'},
}


class Post(models.Model):
    """User post with optional group association."""
    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
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

    def save(self, *args, **kwargs):
        raw_html = _md.render(self.message)
        self.message_html = nh3.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            url_schemes={'http', 'https'},
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
