from django.urls import path

from registration.apps import RegistrationConfig
from registration.services import get_free_records
from registration.views import (
    PersonalAccountViews,
    RegistrationCreate,
    RegistrationDelete,
    RegistrationDetail,
    RegistrationList,
    RegistrationUpdate,
)

app_name = RegistrationConfig.name

urlpatterns = [
    path("registration/", RegistrationList.as_view(), name="registration_list"),
    path(
        "registration/create/", RegistrationCreate.as_view(), name="registration_form"
    ),
    path(
        "registration/<int:pk>/",
        RegistrationDetail.as_view(),
        name="registration_detail",
    ),
    path(
        "registration/<int:pk>/update/",
        RegistrationUpdate.as_view(),
        name="registration_update",
    ),
    path(
        "registration/<int:pk>/delete/",
        RegistrationDelete.as_view(),
        name="registration_delete",
    ),
    path(
        "registration/personal_account",
        PersonalAccountViews.as_view(),
        name="personal_account",
    ),
    path("get-free-records/", get_free_records, name="get_free_records"),
]
