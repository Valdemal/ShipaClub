from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar','slug')
    list_display_links =('user',)
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)
