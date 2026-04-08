from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django import forms

from groups.models import Group, GroupMember


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    """Create a new group."""
    fields = ['name', 'description']
    model = Group


class SingleGroup(generic.DetailView):
    """Display a single group with its posts."""
    model = Group


class ListGroups(generic.ListView):
    """List all groups."""
    model = Group
    paginate_by = 20


# Empty form for CSRF protection on join/leave actions
class EmptyForm(forms.Form):
    pass


class JoinGroup(LoginRequiredMixin, generic.View):
    """Join a group. Uses POST for CSRF protection."""

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=request.user, group=group)
        except IntegrityError:
            messages.warning(
                request, f'Warning: already a member of {group.name}!')
        else:
            messages.success(request, f'You are now a member of {group.name}!')
        return generic.RedirectView.as_view(
            url=reverse('groups:single', kwargs={'slug': group.slug})
        )(request)

    def get(self, request, *args, **kwargs):
        """GET requests redirect to group page (for direct URL access)."""
        return generic.RedirectView.as_view(
            url=reverse('groups:single', kwargs={'slug': kwargs.get('slug')})
        )(request)


class LeaveGroup(LoginRequiredMixin, generic.View):
    """Leave a group. Uses POST for CSRF protection."""

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            membership = GroupMember.objects.filter(
                user=request.user,
                group__slug=slug
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(request, 'Sorry, you are not in this group!')
        else:
            membership.delete()
            messages.success(request, 'You have left the group!')
        return generic.RedirectView.as_view(
            url=reverse('groups:single', kwargs={'slug': slug})
        )(request)

    def get(self, request, *args, **kwargs):
        """GET requests redirect to group page (for direct URL access)."""
        return generic.RedirectView.as_view(
            url=reverse('groups:single', kwargs={'slug': kwargs.get('slug')})
        )(request)
