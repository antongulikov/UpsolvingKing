from django.contrib import admin
from models import Problem

# Register your models here.

class ProblemsAdmin(admin.ModelAdmin):
    fields = ['problem_name', 'contest_id', 'problem_id']
    list_filter = ['contest_id']
    list_display = ['contest_id', 'problem_name']

admin.site.register(Problem, ProblemsAdmin)
