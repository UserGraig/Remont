from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, Master, Order,Speciality

admin.site.register(Client)
admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Speciality)
