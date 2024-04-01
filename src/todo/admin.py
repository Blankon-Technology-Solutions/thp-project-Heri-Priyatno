from django.contrib import admin

from todo.models import Todo


# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed')


# Register your models here.

admin.site.register(Todo, TodoAdmin)
