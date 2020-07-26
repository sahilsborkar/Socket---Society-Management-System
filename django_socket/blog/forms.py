from django import forms
from societies.models import Society

class SocietyJoinForm(forms.ModelForm):
    class Meta:
        model = Society
        exclude = {'name', 'description', 'members'}

class SocietyLeaveForm(forms.ModelForm):
    class Meta:
        model = Society
        exclude = {'name', 'description', 'members'}