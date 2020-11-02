from django.shortcuts import render
from .models import Post

# Create your views here.

posts = [
    {
        'author': 'Matina Bajracharya',
        'title': 'Blog Post 1',
        'content': 'First post',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Matina Bajracharya',
        'title': 'Blog Post 1',
        'content': 'First post',
        'date_posted': 'August 27, 2018'
    }
]




def home(request):
    return render(request, 'forum/home.html', {'title': 'Home'})

def about(request):
    return render(request, 'forum/about.html', {'title': 'About'})

def forum(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Forum'
    }
    return render(request, 'forum/forum.html', context)