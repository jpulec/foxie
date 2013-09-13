from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    text = models.CharField(max_length=140)

    def __unicode__(self):
        return self.text

class Yip(models.Model):
    text = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    dt   = models.DateTimeField(auto_now_add=True)

    def get_words(self):
        return self.text.split(' ')

    def __unicode__(self):
        return "User " + str(self.user) + " yipped " + self.text


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    followee = models.ForeignKey(User, related_name='followee')

    def __unicode__(self):
        return str(self.follower) + " is following " + str(self.followee)
