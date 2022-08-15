from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, Profile

# Update the UserAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ['email', 'username']
    
# Register the users app models
admin.site.register(CustomUser, CustomUserAdmin) 
admin.site.register(Profile) 

