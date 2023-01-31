from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    post_title = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['post_title', 'category', 'author', 'post_text']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class NewsForm(forms.ModelForm):
    post_title = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['post_title', 'category', 'author', 'post_text']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
