from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:# if the user is authenticated user is redirected to project details
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_func