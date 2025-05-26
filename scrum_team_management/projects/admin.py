from django.contrib import admin
from .models import Project, ProjectUpdate

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('testers',)

@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'what_was_done', 'how_project_is_going', 'setbacks', 'created_at')