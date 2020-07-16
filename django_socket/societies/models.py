from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Society(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    members = models.ManyToManyField(User, verbose_name=("Members"))
    # image = models.ImageField(upload_to='society_pics')

    def __str__(self):
        return f"{self.name}"