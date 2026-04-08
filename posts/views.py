"""Post views with type hints and async support."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from posts import models

if TYPE_CHECKING:
    from accounts.models import User as UserType

User = get_user_model()


class PostList(generic.ListView):
    """List all posts with related user and group.

    Note: Using sync ListView is preferred over async View for simple CRUD operations.
    Django 5.x async ORM methods (aget, aiterator) are better suited for:
    - Long-running I/O operations
    - Streaming responses
    - WebSocket handlers
    - Views that aggregate multiple async calls

    For standard database queries with pagination, sync views with proper
    select_related/prefetch_related are more maintainable and performant.
    """

    model = models.Post
    template_name = 'posts/post_list.html'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[models.Post]:
        return super().get_queryset().select_related('user', 'group').order_by('-created_at')


class UserPost(generic.ListView):
    """List posts by a specific user."""

    model = models.Post
    template_name = 'posts/user_post_list.html'
    paginate_by = 20
    post_user: UserType | None = None

    def get_queryset(self) -> QuerySet[models.Post]:
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist as exc:
            raise Http404 from exc
        return self.post_user.posts.all()  # type: ignore[union-attr]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(generic.DetailView):
    """Display a single post."""

    model = models.Post

    def get_queryset(self) -> QuerySet[models.Post]:
        return (
            super()
            .get_queryset()
            .select_related('user', 'group')
            .filter(user__username__iexact=self.kwargs.get('username'))
        )


class CreatePost(LoginRequiredMixin, generic.CreateView):
    """Create a new post."""

    fields = ('message', 'group')
    model = models.Post

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    """Delete a post (only by owner)."""

    model = models.Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self) -> QuerySet[models.Post]:
        return super().get_queryset().select_related('user', 'group').filter(user_id=self.request.user.id)

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, 'Post Deleted')
        return super().form_valid(form)
