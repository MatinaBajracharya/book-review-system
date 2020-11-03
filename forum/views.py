from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

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

class PostListView(ListView):
    model = Post
    template_name = 'forum/forum.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/forum'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    