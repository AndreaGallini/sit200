from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import os
from apps.core.forms import CustomUserCreationForm
from .models import UserAccessLog
from django.urls import reverse
from django.utils.html import format_html

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email'),
        }),
    )
    list_display = ('username', 'email', 'log_count')

    def log_count(self, obj):
        count = obj.access_logs.count()
        url = reverse('admin:core_useraccesslog_changelist') + f'?user__id__exact={obj.id}'
        return format_html('<a href="{}">{} log</a>', url, count)
    log_count.short_description = 'Log'
@admin.register(UserAccessLog)
class UserAccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'location', 'access_time')
    search_fields = ('user__username', 'device', 'location')
    list_filter = ('user', 'access_time')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
