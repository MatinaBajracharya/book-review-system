from django.urls import path
from django.conf.urls import url
from . import views
from .views import like_post, PostListView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', views.home, name='home'),
    path('like/', like_post, name='likes'),
    path('browse/', views.browse, name='browse'),
    path('forum/', PostListView.as_view(), name='forum'),
    path('post/<int:pk>/', views.details, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    url(r'^results/$', views.forum, name="search"),
]
