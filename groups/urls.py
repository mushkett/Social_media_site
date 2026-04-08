from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from groups import views

app_name = 'groups'

# Unicode-compatible slug pattern (matches Cyrillic and other Unicode chars)
_SLUG = r'(?P<slug>[-\w]+)'

urlpatterns = [
    path('', cache_page(60 * 5)(views.ListGroups.as_view()), name='all'),
    path('new/', views.CreateGroup.as_view(), name='create'),
    re_path(r'^posts/in/' + _SLUG + r'$', views.SingleGroup.as_view(), name='single'),
    re_path(r'^join/' + _SLUG + r'/$', views.JoinGroup.as_view(), name='join'),
    re_path(r'^leave/' + _SLUG + r'/$', views.LeaveGroup.as_view(), name='leave'),
    re_path(r'^delete/' + _SLUG + r'/$', views.DeleteGroup.as_view(), name='delete'),
]
