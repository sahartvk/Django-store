from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email_active_code = models.CharField(max_length=63)

    def __str__(self):
        return self.get_full_name