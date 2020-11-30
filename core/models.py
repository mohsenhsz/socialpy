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
        return reverse('post_details', args=[self.publish_date.year,
                        self.publish_date.month, self.publish_date.day, self.slug])
