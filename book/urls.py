from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns=[
    # path('browse/', BookListView.as_view(template_name='browse.html'), name='browse'),
    path('browse/', book_list, name='browse'),
    path('browse/<int:pk>/', detail, name='book-detail'),
    path('history/', history, name='history'),
    url(r'^books/$', searchbook, name="searchbook"),
    path('autosuggestbook/', autosuggestbook, name='autosuggestbook'),
]