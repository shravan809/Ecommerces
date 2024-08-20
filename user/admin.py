from django.contrib import admin

# Register your models here.
from .models import User

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display=['email','otp','is_verified']