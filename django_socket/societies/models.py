from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Society(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    members = models.ManyToManyField(User, verbose_name=("Members"))
    # image = models.ImageField(upload_to='society_pics')
    def __str__(self):
        return f"{self.name}"

class SocPost(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="posts")
    def __str__(self):
        return self.title