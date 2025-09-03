# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)  # 👈 this must exist
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username