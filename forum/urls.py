from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='forum-home'),
    path('about/', views.about, name='forum-about'),
    path('forum/', views.forum, name='forum-page'),
]
