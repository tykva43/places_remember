from django.contrib.auth.models import User
from django.db import models


# Memory Model
class Memo(models.Model):
    place = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    commentary = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
