from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from societies.models import Society, SocPost
from django.urls import reverse_lazy

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

@login_required
def sochome(request, oid):
    society = Society.objects.filter(id=oid).first()
    context = {
        'society': society,
        'posts': society.posts.all().order_by('-date_posted')
    }
    return render(request, 'blog/sochome.html', context)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = SocPost
    template_name = 'blog/socpost_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = SocPost
    fields = ['title', 'content']
    template_name = 'blog/socpost_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.society = Society.objects.filter(pk=self.kwargs.get('society_id')).first()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SocPost
    fields = ['title', 'content']
    template_name = 'blog/socpost_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.society = Society.objects.filter(pk=self.kwargs.get('society_id')).first()
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocPost
    template_name = 'blog/socpost_confirm_delete.html'
    #success_url = get_success_url()

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('blog-sochome', kwargs={'oid':post.society.id})
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False