from django.forms import ModelForm
from .models import Society

class SocietyRegisterForm(ModelForm):
    class Meta:
        model = Society
        fields = ['name', 'description']