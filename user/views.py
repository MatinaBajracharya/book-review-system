from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from forum.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome to our community { username }! Please login to continue.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def EditProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated.')
            return redirect('profile', pk = request.user.id)
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)
    
    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user/edit-profile.html', context)

def profile(request, pk):
    u_id = User.objects.get(pk=pk)
    post = Post.objects.filter(author = pk).order_by('-date_posted')

    context={
        'title': 'Profile',
        'u_id' : u_id,
        'posts' : post,
    }
    return render(request, 'forum/profile.html', context)