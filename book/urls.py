from django.urls import path
from .views import *

urlpatterns=[
    path('browse/', BookListView.as_view(template_name='browse.html'), name='browse'),
]