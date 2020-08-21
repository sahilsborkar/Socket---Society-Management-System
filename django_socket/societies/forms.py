from django.forms import ModelForm
from .models import Society, SocietyProfile, SocComment

class SocietyRegisterForm(ModelForm):
    class Meta:
        model = Society
        fields = ['name', 'description']

class SocietyUpdateForm(ModelForm):
    class Meta:
        model = Society
        fields = ['name', 'description']

class SocietyProfileUpdateForm(ModelForm):

    class Meta:
        model = SocietyProfile
        fields = ['image']

class CommentCreateForm(ModelForm):
    class Meta:
        model = SocComment
        fields = ['content']
