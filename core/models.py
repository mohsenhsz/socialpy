from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=200, allow_unicode=True)
    publish_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-{self.content[:30]}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_details', args=[self.pk, self.publish_date.year,
                        self.publish_date.month, self.publish_date.day, self.slug])

    def likes_count(self):
        all_likes = self.pvote.count()
        return all_likes

    def user_can_like(self, user):
        user_likes = user.uvote.all()
        qs = user_likes.filter(post=self)
        if qs.exists():
            return False
        else:
            return True


class Comment(models.Model):
    """ Disallow backward relation: related_name='+' """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-{self.post.content[:20]}'

    class Meta:
        ordering = ('date',)


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvote')

    def __str__(self):
        return f'{self.user} Liked {self.post}'
