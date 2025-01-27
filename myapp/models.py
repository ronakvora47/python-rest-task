from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    city = models.CharField(max_length=99)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk and not CustomUser.objects.filter(is_admin=True).exists():
            self.is_admin = True 
        super().save(*args, **kwargs)

    

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)