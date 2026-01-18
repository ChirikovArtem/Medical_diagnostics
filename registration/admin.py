from django.contrib import admin

from registration.models import Registration


@admin.register(Registration)
class ReservationAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели регистрации"""

    list_display = (
        "id",
        "date_registration",
        "time_registration",
        "patient",
        "registration",
    )
    list_filter = (
        "date_registration",
        "patient",
        "registration",
    )
    search_fields = (
        "date_registration",
        "patient",
        "registration",
    )