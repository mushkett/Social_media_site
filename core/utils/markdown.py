"""
Markdown rendering utilities with HTML sanitization.

Uses markdown-it-py for rendering and nh3 for XSS protection.
"""

from __future__ import annotations

import nh3
from markdown_it import MarkdownIt

# Singleton markdown renderer
_md = MarkdownIt()

# Allowed HTML tags for sanitized markdown output
ALLOWED_TAGS: set[str] = {
    'a',
    'abbr',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'pre',
    'strong',
    'ul',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'br',
    'hr',
    'img',
    'table',
    'thead',
    'tbody',
    'tr',
    'th',
    'td',
}

# Allowed attributes per tag
ALLOWED_ATTRIBUTES: dict[str, set[str]] = {
    'a': {'href', 'title'},
    'abbr': {'title'},
    'img': {'src', 'alt', 'title'},
}

# Allowed URL schemes
ALLOWED_URL_SCHEMES: set[str] = {'http', 'https', 'mailto'}


def render_markdown(text: str) -> str:
    """
    Render markdown text to sanitized HTML.

    Args:
        text: Raw markdown text

    Returns:
        Sanitized HTML string safe for rendering

    Example:
        >>> render_markdown("**bold** and *italic*")
        '<p><strong>bold</strong> and <em>italic</em></p>'
    """
    if not text:
        return ''

    raw_html = _md.render(text)
    return nh3.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
    )
