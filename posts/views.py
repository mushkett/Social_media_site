from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404

from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(generic.ListView):
    """List all posts with related user and group."""
    model = models.Post

    def get_queryset(self):
        return super().get_queryset().select_related('user', 'group')


class UserPost(generic.ListView):
    """List posts by a specific user."""
    model = models.Post
    template_name = 'posts/user_post_list.html'
    post_user = None

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username')
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(generic.DetailView):
    """Display a single post."""
    model = models.Post

    def get_queryset(self):
        return super().get_queryset().select_related('user', 'group').filter(
            user__username__iexact=self.kwargs.get('username')
        )


class CreatePost(LoginRequiredMixin, generic.CreateView):
    """Create a new post."""
    fields = ('message', 'group')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    """Delete a post (only by owner)."""
    model = models.Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        return super().get_queryset().select_related('user', 'group').filter(
            user_id=self.request.user.id
        )

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
