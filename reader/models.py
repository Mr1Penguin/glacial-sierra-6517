from django.db import models

# Create your models here.

class User(models.Model):
    user_email = models.EmailField()
    password = models.CharField(max_length=255)
    def __unicode__ (self):
        return self.user_email

class User_token(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    last_use = models.DateTimeField()

class Site(models.Model):
    url = models.URLField(max_length=2000)
    favicon = models.URLField(max_length=2000, null=True)
    add_date = models.DateTimeField()
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=True)

class Image(models.Model):
    url = models.URLField(max_length=2000)
    site = models.ForeignKey(Site)
    add_date = models.DateTimeField()
    width = models.IntegerField(default=600)

#check add date string if none exists
class Collect(models.Model):
    collect_date = models.DateTimeField()
