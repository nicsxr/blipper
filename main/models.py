from django.db import models
from account.models import Account

class Post(models.Model):
    poster = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(default='', max_length=255)
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(verbose_name='date posted', auto_now_add=True)
    likers = models.ManyToManyField(Account, related_name="likers")
    objects = models.Manager()

    def __str__(self):
        return self.poster + " " + self.date_posted

