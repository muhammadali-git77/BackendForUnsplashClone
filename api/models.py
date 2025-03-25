from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    subtitle = models.CharField(max_length=20)

    def __str__(self):
        return self.subtitle

    def get_download_url(self):
        if self.image:
            return settings.MEDIA_URL + str(self.image)
        return None
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username