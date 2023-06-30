from django.contrib import admin

from .models import User,UserPersonalData,Visitor


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']


admin.site.register(User, UserAdmin)
admin.site.register(UserPersonalData)
admin.site.register(Visitor)
