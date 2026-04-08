from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from django_ratelimit.decorators import ratelimit

from accounts import forms


@method_decorator(ratelimit(key='ip', rate='10/h', method='POST', block=True), name='post')
class Login(auth_views.LoginView):
    """Login view with rate limiting: max 10 attempts per IP per hour."""

    template_name = 'accounts/login.html'


@method_decorator(ratelimit(key='ip', rate='5/h', method='POST', block=True), name='post')
class SignUp(CreateView):
    """Sign up view with rate limiting: max 5 registrations per IP per hour."""

    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
