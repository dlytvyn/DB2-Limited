from django import forms
from .models import Posts, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'post_body',
            'photo'
        ]

    def save(self, request, commit=True):
        self.instance.user = request.user
        return super().save(commit)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_text']

    def save(self, request, post, commit=True):
        self.instance.author = request.user
        self.instance.post = post
        return super().save(commit)
