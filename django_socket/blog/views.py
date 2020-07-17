from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from societies.models import Society
# Create your views here.

def home(request):
    return render(request, 'blog/intro.html')

@login_required
def soclist(request):
    current_user = request.user
    context = {
        'societies':current_user.society_set.all()
    }
    return render(request, 'blog/soclist.html', context)

#@login_required
#def sochome(request):
#    context = {
#        'posts': Post.objects.all(),
#        'title': 'Home'
#    }
#    return render(request, 'blog/sochome.html', context)

#@login_required
#def sochome(request):
#    if request.method == 'GET':
#        society = request.GET.get('society')
#        if not society:
#            return render(request, 'blog/soclist.html')
#        else:
#            context = {
#                'society': society,
#                'name': society.name,
#                'description': society.description
#            }
#            return render(request, 'blog/sochome.html', context)

@login_required
def sochome(request, oid):
    society = Society.objects.filter(id=oid).first()
    context = {
        'society': society,
        'posts': society.posts.all()
    }
    return render(request, 'blog/sochome.html', context)
