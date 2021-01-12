from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Like, Comment, SubComment
from django.contrib.auth.models import User
from .decorators import authenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# Create your views here.

def home(request):
    return render(request, 'forum/home.html', {'title': 'Home'})

def browse(request):
    return render(request, 'forum/browse.html', {'title': 'Browse'})

@login_required
def forum(request):
    context = {
        'posts': Post.objects.all(),
        'comment': Comment.object.all().count(),
        'title': 'Forum'
    }
    return render(request, 'forum/forum.html', context)

@login_required
def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user = user, post_id = post_id)
        if not created:
            if like.value == 'Like':
                like.value == 'Unlike'
            else:
                like.value = 'Like'
            like.save()
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PostListView(ListView):
    model = Post
    template_name = 'forum/forum.html'
    context_object_name = 'posts'
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'forum/profile.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User)
        return Post.objects.filter(author=user).order_by('-date_posted')

# class PostDetailView(DetailView):
#     model = Post

def details(request, pk):
    template = "forum/post_detail.html"
    try:
        post = get_object_or_404(Post, pk=pk)
        # details = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-id')
    except Post.DoesNotExist:
        raise Http404("Post does not exist.")

    if request.method == 'POST':
        comment = request.POST.get('comm') 
        comm_id = request.POST.get('comm_id')

        if comm_id:
            SubComment(post=post,
                user = request.user,
                comment = comment,
                comment_reply = Comment.objects.get(id=int(comm_id))
            ).save()
        else:
            Comment(post=post, user = request.user, comment=comment).save()

    comments = []
    for c in Comment.objects.filter(post=post):
        comments.append([c, SubComment.objects.filter(comment_reply = c)])


    # user = request.user
    # if request.method == 'POST':
    #     post_id = pk
    #     post_obj = Post.objects.get(id = post_id)

    #     if user in post_obj.likes.all():
    #         post_obj.likes.remove(user)
    #     else:
    #         post_obj.likes.add(user)

    #     like, created = Like.objects.get_or_create(user = user, post_id = post_id)
    #     if not created:
    #         if like.value == 'Like':
    #             like.value == 'Unlike'
    #         else:
    #             like.value = 'Like'
    #         like.save()
    #     return redirect('post-detail', pk=pk)


    context = {
        'object' : post,
        'comments' :comments,
        # 'comment_form' : comment_form,
    }
    return render(request, template, context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    widgets ={
        'content':SummernoteInplaceWidget(),
        }

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

    