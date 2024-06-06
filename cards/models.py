from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    censored_number = models.CharField(max_length=16)
    is_valid = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

