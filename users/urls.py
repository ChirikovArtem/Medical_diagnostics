from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import (
    UserCreateViews,
    UserDelete,
    UserDetailView,
    UserListView,
    UserUpdateView,
    email_verification,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "users/base/", LoginView.as_view(template_name="users/base.html"), name="base"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateViews.as_view(), name="user_form"),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("user_detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users_update/<int:pk>/", UserUpdateView.as_view(), name="users_update"),
    path("users_delete/<int:pk>/", UserDelete.as_view(), name="user_delete"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
