from django.db import models

# Create your models here.


class Yip(models.Model):
    text = models.CharField(max_length=140)
    user = models.ForeignKey('User')
