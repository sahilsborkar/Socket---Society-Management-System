from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from societies.models import Society, SocPost, SocietyMembership
from django.urls import reverse_lazy
from .forms import SocietyJoinForm, SocietyLeaveForm, SocietyManageForm
from django.contrib import messages
from django.db.models.functions import Lower


def home(request):
    return render(request, 'blog/intro.html')

@login_required
def soclist(request):
    current_user = request.user
    leader_memberships = SocietyMembership.objects.filter(member=current_user, is_leader=True)
    normal_memberships = SocietyMembership.objects.filter(member=current_user, is_leader=False)
    context = {
        'societies':current_user.societies.all(),
        'leader_memberships': leader_memberships,
        'normal_memberships': normal_memberships
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
    paginate_by = 15
    
    def get_queryset(self):
        user = self.request.user
        joined_societies = user.societies.all()

        qs = super().get_queryset()
        return qs.exclude(id__in=joined_societies)

def society_join(request, society_id):
    society = Society.objects.filter(id=society_id).first()
    user = request.user
    if request.method == 'POST':
        form = SocietyJoinForm(request.POST)
        if form.is_valid():
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

class SocietyManageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
        
    model = SocietyMembership
    template_name = 'blog/socmanage.html'
    context_object_name = 'memberships'
    paginate_by = 10

    def test_func(self):
        society = Society.objects.get(pk=self.kwargs.get('society_id'))
        return (society.is_member(self.request.user) and society.user_is_leader(self.request.user))

    def get_queryset(self):
        society = Society.objects.get(pk=self.kwargs.get('society_id'))
        qs = super().get_queryset()
        return qs.filter(society=society)

    def get_context_data(self, **kwargs):
        society = Society.objects.get(pk=self.kwargs.get('society_id'))
        memberships = SocietyMembership.objects.filter(society=society)
        context = super(ListView, self).get_context_data(**kwargs)
        context['society'] = society
        return context

    def post(self, request, *args, **kwargs):
        society = Society.objects.get(pk=self.kwargs.get('society_id'))
        if request.POST:
            if 'promote' in request.POST:
                member = User.objects.filter(id=request.POST.get('promote', '')).first()
                society.promote(member)
                messages.success(request, f'You have promoted {member.first_name}!')
                return redirect('society-manage', self.kwargs['society_id'])
            elif 'demote' in request.POST:
                member = User.objects.filter(id=request.POST.get('demote', '')).first()
                society.demote(member)
                messages.success(request, f'You have demoted {member.first_name}!')
                return redirect('society-manage', self.kwargs['society_id'])
            elif 'kick' in request.POST:
                member = User.objects.filter(id=request.POST.get('kick', '')).first()
                society.kick(member)
                messages.success(request, f'You have removed {member.first_name}!')
                return redirect('society-manage', self.kwargs['society_id'])


