from django import forms
from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', )


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }
        labels = {
            'body': ('Leave a comment'),
        }
        error_messages = {
            'body':{
                'required':'this field is required'
            }
        }
        help_texts = {
            'body':'max 300 characters'
        }


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
