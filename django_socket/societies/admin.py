from django.contrib import admin
from .models import Society, SocPost, SocietyMembership, SocietyProfile

# Register your models here.
admin.site.register(Society)
admin.site.register(SocPost)
admin.site.register(SocietyMembership)
admin.site.register(SocietyProfile)