from django.contrib import admin
from models import UpUser

# Register your models here.

class UpUserAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
    list_filter = ['username']
    list_display = ['username']

admin.site.register(UpUser, UpUserAdmin)
