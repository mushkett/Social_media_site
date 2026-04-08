from django.urls import path, re_path
from groups import views

app_name = 'groups'

# Unicode-compatible slug pattern (matches Cyrillic and other Unicode chars)
_slug = r'(?P<slug>[-\w]+)'

urlpatterns = [
    path('', views.ListGroups.as_view(), name='all'),
    path('new/', views.CreateGroup.as_view(), name='create'),
    re_path(r'^posts/in/' + _slug + r'$', views.SingleGroup.as_view(), name='single'),
    re_path(r'^join/' + _slug + r'/$', views.JoinGroup.as_view(), name='join'),
    re_path(r'^leave/' + _slug + r'/$', views.LeaveGroup.as_view(), name='leave'),
    re_path(r'^delete/' + _slug + r'/$', views.DeleteGroup.as_view(), name='delete'),
]
