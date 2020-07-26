from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from societies.models import Society, SocPost, SocietyMembership
from django.urls import reverse_lazy
from .forms import SocietyJoinForm, SocietyLeaveForm
from django.contrib import messages
from django.db.models.functions import Lower


def home(request):
    return render(request, 'blog/intro.html')

#def is_leader(self):


@login_required
def soclist(request):
    current_user = request.user
    context = {
        'societies':current_user.societies.all()
    }
    return render(request, 'blog/soclist.html', context)

@login_required
def sochome(request, oid):
    society = Society.objects.filter(id=oid).first()
    membership = SocietyMembership.objects.get(member=request.user, society=society)
    context = {
        'membership': membership,
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

class SocietyListView(LoginRequiredMixin, ListView):
    model = Society
    template_name = 'blog/joinsoc.html'
    context_object_name = 'societies'
    ordering = [Lower('name')]
    paginate_by = 20

def society_join(request, society_id):
    society = Society.objects.filter(id=society_id).first()
    user = request.user
    if request.method == 'POST':
        form = SocietyJoinForm(request.POST)
        if form.is_valid():
            # society.members.add(user)
            society.members.add(user, through_defaults={'is_leader':False})
            society_name = society.name
            messages.success(request, f'You have been added to {society_name}!')
            return redirect('join-society')
    else:
        form = SocietyJoinForm()
    context = {
        'society': society,
        'form': form
    }
    return render(request, 'blog/joinsoc_confirm.html', context)

def society_leave(request, society_id):
    society = Society.objects.filter(id=society_id).first()
    user = request.user
    if request.method == 'POST':
        form = SocietyLeaveForm(request.POST)
        if form.is_valid():
            society.members.remove(user)
            society_name = society.name
            messages.success(request, f'You have left {society_name}!')
            return redirect('blog-soclist')
    else:
        form = SocietyLeaveForm()
    context = {
        'society': society,
        'form': form
    }
    return render(request, 'blog/socleave.html', context)

# def society_admin(request, )