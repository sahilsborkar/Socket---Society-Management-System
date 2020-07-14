from django.shortcuts import render
from .models import Post
# Create your views here.

def home(request):
    return render(request, 'blog/intro.html')

def sochome(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/sochome.html', context)