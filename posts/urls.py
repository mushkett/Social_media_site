from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'posts'

urlpatterns = [
    path('', cache_page(60 * 5)(views.PostList.as_view()), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('by/<username>', views.UserPost.as_view(), name='for_user'),
    path("by/<username>/<int:pk>/", views.PostDetail.as_view(), name="single"),
    path("delete/<int:pk>/", views.DeletePost.as_view(), name="delete"),
]
