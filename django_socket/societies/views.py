from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SocietyRegisterForm, SocietyProfileUpdateForm, SocietyUpdateForm
from django.views.generic import UpdateView, FormView
from .models import Society, SocietyProfile, SocietyMembership

@login_required
def society_register(request):
    if request.method == 'POST':
        form = SocietyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            society = Society.objects.filter(name=form.cleaned_data.get('name')).first()
            society.members.add(request.user, through_defaults={'is_leader':True})
            messages.success(request, f'The society {name} has been added!')
            return redirect('blog-soclist')
    else:
        form = SocietyRegisterForm()
    return render(request, 'blog/socregister.html', {'form':form})



@login_required
def society_profile(request, *args, **kwargs):
    society =  Society.objects.filter(id=kwargs['society_id']).first()
    leaders = society.leaders
    membership = SocietyMembership.objects.filter(member=request.user, society=society).first()
    if request.method == 'POST':
        s_form = SocietyUpdateForm(request.POST, instance=society)
        sp_form = SocietyProfileUpdateForm(request.POST, request.FILES, instance=society.profile)
        if s_form.is_valid() and sp_form.is_valid():
            s_form.save()
            sp_form.save()
            messages.success(request, f'{society} has been updated.')
            return redirect('society-profile', kwargs['society_id'])

    else:
        s_form = SocietyUpdateForm(instance=society)
        sp_form = SocietyProfileUpdateForm(instance=society.profile)

    context = {
        's_form':s_form,
        'sp_form':sp_form,
        'society':society,
        'is_a_leader': membership.is_leader
    }
    return render(request, 'societies/socprofile.html', context)