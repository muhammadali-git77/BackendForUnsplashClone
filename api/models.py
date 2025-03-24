from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    subtitle = models.CharField(max_length=20)

    def __str__(self):
        return self.subtitle

    def download_url(self):
        """Rasmni yuklab olish uchun to‘liq URL qaytaradi."""
        if self.image:
            return f"{settings.MEDIA_URL}{self.image}"
        return None
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username