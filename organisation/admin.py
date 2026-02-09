from django.contrib import admin

from organisation.models import Employee, Organisation, Record


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели медицинской организации"""

    list_display = (
        "id",
        "name",
    )
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели услуги"""

    list_display = (
        "id",
        "service",
        "doctor",
    )

    list_filter = (
        "service",
        "doctor",
    )
    search_fields = (
        "service",
        "doctor",
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели сотрудник"""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "job_title",
    )

    list_filter = (
        "last_name",
        "job_title",
    )
    search_fields = (
        "last_name",
        "job_title",
    )
