from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import misaka
import bleach

User = get_user_model()

# Allowed HTML tags for sanitized markdown output
ALLOWED_TAGS = [
    'a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i',
    'li', 'ol', 'p', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3',
    'br', 'hr',
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
}


class Group(models.Model):
    """A group that users can join and post to."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # Convert markdown to HTML and sanitize
        raw_html = misaka.html(self.description)
        self.description_html = bleach.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    """Through model for User-Group M2M relationship."""
    group = models.ForeignKey(
        Group,
        related_name='memberships',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='user_groups',
        on_delete=models.CASCADE
    )
    joined_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'user'],
                name='unique_group_member'
            )
        ]
