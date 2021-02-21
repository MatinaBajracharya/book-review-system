from django import forms
from .models import Post

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class PostForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget = SummernoteWidget())
    class Meta:
        model = Post
        fields = ['title', 'content']