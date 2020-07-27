from django import forms
from societies.models import Society, SocietyMembership

class SocietyJoinForm(forms.ModelForm):
    class Meta:
        model = Society
        exclude = {'name', 'description', 'members'}

class SocietyLeaveForm(forms.ModelForm):
    class Meta:
        model = Society
        exclude = {'name', 'description', 'members'}

class SocietyManageForm(forms.ModelForm):
    class Meta:
        model = SocietyMembership
        exclude = {'society', 'is_leader'}