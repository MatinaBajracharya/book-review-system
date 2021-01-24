from django import forms
# from .models import Review

class ReviewForm(forms.Form):
    comment = forms.CharField(max_length=100)
    rate = forms.IntegerField()
