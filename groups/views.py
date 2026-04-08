"""Group views with type hints."""

from __future__ import annotations

from typing import Any

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from groups.models import Group, GroupMember


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    """Create a new group."""

    fields = ['name', 'description']
    model = Group

    def form_valid(self, form) -> HttpResponse:
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DeleteGroup(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Delete a group. Only the creator can delete it."""

    model = Group
    success_url = '/groups/'

    def get_queryset(self) -> QuerySet[Group]:
        return super().get_queryset().filter(creator=self.request.user)

    def test_func(self) -> bool:
        return self.get_object().creator == self.request.user


class SingleGroup(generic.DetailView):
    """Display a single group with its posts."""

    model = Group

    def get_queryset(self) -> QuerySet[Group]:
        return super().get_queryset().prefetch_related('members', 'posts')


class ListGroups(generic.ListView):
    """List all groups with annotated member and post counts."""

    model = Group
    template_name = 'groups/group_list.html'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Group]:
        return (
            super()
            .get_queryset()
            .select_related('creator')
            .annotate(
                member_count=Count('members', distinct=True),
                post_count=Count('posts', distinct=True),
            )
            .order_by('name')
        )


# Empty form for CSRF protection on join/leave actions
class EmptyForm(forms.Form):
    pass


class JoinGroup(LoginRequiredMixin, generic.View):
    """Join a group. Uses POST for CSRF protection."""

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        group = get_object_or_404(Group, slug=kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=request.user, group=group)  # type: ignore[misc]
        except IntegrityError:
            messages.warning(request, f'Warning: already a member of {group.name}!')
        else:
            messages.success(request, f'You are now a member of {group.name}!')
        return HttpResponseRedirect(reverse('groups:single', kwargs={'slug': group.slug}))

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """GET requests redirect to group page (for direct URL access)."""
        return HttpResponseRedirect(reverse('groups:single', kwargs={'slug': kwargs.get('slug')}))


class LeaveGroup(LoginRequiredMixin, generic.View):
    """Leave a group. Uses POST for CSRF protection."""

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        slug = kwargs.get('slug')
        try:
            membership = GroupMember.objects.filter(
                # type: ignore[misc]
                user=request.user,
                group__slug=slug,
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(request, 'Sorry, you are not in this group!')
        else:
            membership.delete()
            messages.success(request, 'You have left the group!')
        return HttpResponseRedirect(reverse('groups:single', kwargs={'slug': slug}))

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """GET requests redirect to group page (for direct URL access)."""
        return HttpResponseRedirect(reverse('groups:single', kwargs={'slug': kwargs.get('slug')}))
