from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', )


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
