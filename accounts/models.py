from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s" + ' Profile'


"""
kwargs--->{
            'created':'Is a boolean that contains the post_save status',
            'instance': 'Contains a copy of the saved object'
               }
               """
@receiver(post_save, sender=User)     # post_save.connect(save_profile, sender=User)
def save_profile(sender, **kwargs):
    if kwargs['created']:
        p1 = Profile(user=kwargs['instance'])
        p1.save()
