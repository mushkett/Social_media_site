from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import nh3
from markdown_it import MarkdownIt

User = get_user_model()

_md = MarkdownIt()

# Allowed HTML tags for sanitized markdown output
ALLOWED_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i',
    'li', 'ol', 'p', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3',
    'br', 'hr',
}
ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title'},
}


class Group(models.Model):
    """A group that users can join and post to."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')
    creator = models.ForeignKey(
        User,
        related_name='created_groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        # Convert markdown to HTML and sanitize
        raw_html = _md.render(self.description)
        self.description_html = nh3.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            url_schemes={'http', 'https'},
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
