from django.contrib import admin
from models import UpUser, Tag, Problem, TagProblem, UserTag

# Register your models here.

class UpUserAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
    list_filter = ['username']
    list_display = ['username']

admin.site.register(UpUser, UpUserAdmin)

class TagAdmin(admin.ModelAdmin):
    fields = ['name']
    list_filter =  ['name']
    list_display = ['name']

admin.site.register(Tag, TagAdmin)

class TagProblemAdmin(admin.ModelAdmin):
    fields = ['tag', 'problem', 'cnt_solved']
    list_filter = ['cnt_solved']
    list_display = ['tag', 'problem', 'cnt_solved']

class ProblemAdmin(admin.ModelAdmin):
    fields = ['problem_name', 'contest_id', 'solved']
    list_filter = ['contest_id']
    list_display = ['problem_name', 'contest_id', 'solved']

admin.site.register(Problem, ProblemAdmin)
admin.site.register(TagProblem, TagProblemAdmin)

class UserTagAdmin(admin.ModelAdmin):
    fields = ['user', 'tag', 'power']
    list_filter = ['user', 'power']
    list_display = ['user', 'tag', 'power']

