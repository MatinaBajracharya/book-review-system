from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Like, Comment, SubComment
from django.contrib.auth.models import User
from .decorators import authenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import PostForm
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'forum/home.html', {'title': 'Home'})

@login_required
def forum(request):
    query = request.GET.get('q')

    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query))
    else:
        results = Post.objects.all()
        
    try:
        paginator = Paginator(results, 4)  # 3 posts in each page
        page = request.GET.get('page')
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except:
        raise Http404("Something went wrong.")

    context = {
        'title': 'Forum',
        'page_obj': page_obj,
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

        data = {
            'value': like.value,
            'likes': post_obj.likes.all().count()
        }
        return JsonResponse(data, safe=False)
    # return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostListView(ListView):
    model = Post
    template_name = 'forum/forum.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']

class UserPostListView(ListView):
    model = Post
    template_name = 'forum/profile.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User)
        return Post.objects.filter(author=user).order_by('-date_posted')

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
            return JsonResponse({
                'msg': 'Success'
            })
        else:
            Comment(post=post, user = request.user, comment=comment).save()
            return JsonResponse({
                'msg': 'Success'
            })

    comments = []
    for c in Comment.objects.filter(post=post):
        comments.append([c, SubComment.objects.filter(comment_reply = c)])

    context = {
        'object' : post,
        'comments' :comments,
        # 'comment_form' : comment_form,
    }
    return render(request, template, context)

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'forum/post_form.html'
    form_class = PostForm
    queryset = Post.objects.all()
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'forum/post_form.html'
    form_class = PostForm
    queryset = Post.objects.all()
    
    def form_valid(self,form):
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

def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Post.objects.filter(Q(title__icontains=query_original))
    mylist = []
    mylist += [x.title for x in queryset]
    return JsonResponse(mylist, safe=False)

