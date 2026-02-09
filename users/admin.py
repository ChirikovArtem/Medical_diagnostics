from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели пользователя"""

    list_display = ("id", "email", "last_name", "first_name")
