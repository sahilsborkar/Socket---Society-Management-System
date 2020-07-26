from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SocietyRegisterForm
from .models import Society

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
