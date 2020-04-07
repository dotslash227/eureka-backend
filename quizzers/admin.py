from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Club, Category

# Profile administration to be embedded into already existing user
# admin
class ProfileAdmin(admin.StackedInline):
    model = Profile

# Registering mutated admin panel
class NewUserAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "email", "date_joined"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["username", "first_name", "last_name"]
    inlines = [ProfileAdmin]

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)


# Admin settings for clubs
class ClubAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on", "creator", "category"]
    list_filter = ["created_on", "category"]

admin.site.register(Club, ClubAdmin)
admin.site.register(Category)
