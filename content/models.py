from django.db import models
from django.utils.translation import gettext_lazy as _


class Comments(models.Model):
    author = models.ForeignKey('accounts.User', related_name='comments', on_delete=models.CASCADE)
    comment_text = models.CharField(_('comment_text'), max_length=256, blank=True)
    post = models.ForeignKey('Posts', related_name='comments', on_delete=models.CASCADE)


class Likes(models.Model):
    post = models.ForeignKey('Posts', related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', related_name='likes', on_delete=models.CASCADE)


class Posts(models.Model):
    title = models.CharField(_('title'), max_length=50, blank=True)
    post_body = models.CharField(_('post_body'), max_length=256, blank=True)
    photo = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name='post_photo')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    @property
    def liked_users(self):
        return [like.user for like in self.likes.all()]
