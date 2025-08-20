from django.contrib import admin
from .models import Counter, Project


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_code', 'user_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('project_code', 'user_id__username')
    readonly_fields = ('created_at',)
