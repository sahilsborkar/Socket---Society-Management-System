from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Society(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    members = models.ManyToManyField(User, verbose_name=("Members"))

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def create(cls, **kwargs):
        society = cls.objects.create(
            name=kwargs['name'],
            description=kwargs['description']
        )
        return society

class SocPost(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'society_id':self.society.id, 'pk':self.pk})