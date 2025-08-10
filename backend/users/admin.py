from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 리스트/폼에서 보일 필드를 약간 손보면 좋음
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("nickname",)}),
    )
    