from django.contrib import admin
from .models import Project, ProjectUpdate

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('project', 'update_text', 'created_at')
    list_filter = ('project',)
    search_fields = ('update_text',)