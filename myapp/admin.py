from django.contrib import admin
from .models import User,Doctor_Profile,Appointment
# Register your models here.
admin.site.register(User)
admin.site.register(Doctor_Profile)
admin.site.register(Appointment)