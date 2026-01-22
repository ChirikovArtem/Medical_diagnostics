from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from organisation import views
from organisation.apps import OrganisationConfig
from organisation.views import (AboutOrganisationViews, ContactsViews,
                                EmployeeCreate, EmployeeDelete, EmployeeDetail,
                                EmployeeList, EmployeeUpdate, FeedbackViews,
                                HomeViews, OrganisationUpdate, RecordCreate,
                                RecordDelete, RecordDetail, RecordList,
                                RecordUpdate, ServicesViews,
                                SiteManagementViews)

app_name = OrganisationConfig.name


urlpatterns = [
    path("home", HomeViews.as_view(), name="home"),
    path("organisation/", AboutOrganisationViews.as_view(), name="organisation"),
    path(
        "organisation/<int:pk>/update/",
        OrganisationUpdate.as_view(),
        name="organisation_update",
    ),
    path("organisation/services/", ServicesViews.as_view(), name="services"),
    path("organisation/contacts/", ContactsViews.as_view(), name="contacts"),
    path("organisation/feedback/", FeedbackViews.as_view(), name="feedback"),
    path(
        "organisation/feedback/submit/", views.feedback_submit, name="feedback_submit"
    ),
    path(
        "organisation/site_management/",
        SiteManagementViews.as_view(),
        name="site_management",
    ),
    path("employee/", EmployeeList.as_view(), name="employee_list"),
    path("employee/<int:pk>/", EmployeeDetail.as_view(), name="employee_detail"),
    path("employee/create/", EmployeeCreate.as_view(), name="employee_create"),
    path("employee/<int:pk>/delete/", EmployeeDelete.as_view(), name="employee_delete"),
    path("employee/<int:pk>/update/", EmployeeUpdate.as_view(), name="employee_update"),
    path("record/<int:pk>/", RecordDetail.as_view(), name="record_detail"),
    path("record/", RecordList.as_view(), name="record_list"),
    path("record/create/", RecordCreate.as_view(), name="record_create"),
    path("record/<int:pk>/delete/", RecordDelete.as_view(), name="record_delete"),
    path("record/<int:pk>/update/", RecordUpdate.as_view(), name="record_update"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
