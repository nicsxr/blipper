from django.db import models
from account.models import Account

class Post(models.Model):
    poster = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(default='', max_length=255)
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(verbose_name='date posted', auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.poster + " " + self.date_posted

    def upvoters(self):
        return Like.objects.filter(post=self).values_list('liker', flat=True)


class Like(models.Model):
	liker = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='liker')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
	like_time = models.DateTimeField(auto_now=True)

	objects = models.Manager()

	class Meta:
		unique_together = (('liker', 'post'),)
	