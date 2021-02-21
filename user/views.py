from django.shortcuts import render, redirect
from django.contrib.auth import logout
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

def DeleteProfile(request, pk):
    u_id = request.user.id
    profile_uid = User.objects.get(pk = pk)
    p_id = profile_uid.id
    print(p_id)
    print(u_id)
    if request.method == 'POST':
        if p_id == u_id:
            profile_uid.delete()
            logout(request)
            messages.success(request, f'User has been deleted')
            return redirect('register')
    else:
        messages.error(request, f'You are not authorized to delete users!')
        return redirect('browse')


@login_required
def profile(request, pk):
    u_id = User.objects.get(pk=pk)
    post = Post.objects.filter(author = pk).order_by('-date_posted')

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
        'title': 'Profile',
        'u_id' : u_id,
        'posts' : post,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'forum/profile.html', context)