import secrets

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserCreateViews(CreateView):
    """Контроллер для создания пользователя"""

    template_name = "users/user_form.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"

        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, для регистрации почты {url} перейдите по ссылке",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        messages.success(
            self.request, "Письмо с подтверждением отправлено на ваш email."
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.token = None
    user.is_active = True
    user.save()
    messages.success(request, "Ваш email успешно подтверждён!")
    return redirect(reverse("users:login"))


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер отображения списка пользователей"""

    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    permission_required = "users.view_user"

    def get_queryset(self):
        """Исключение из списка суперпользователя и всех менеджеров"""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False)
        queryset = queryset.exclude(groups__permissions__codename="can_change_content")
        return queryset


class UserDetailView(DetailView):
    """Контроллер отображения профиля пользователя"""

    model = User
    template_name = "users/user_detail.html"
    context_object_name = "users"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования профиля пользователя"""

    model = User
    form_class = UserUpdateForm
    template_name = "users/users_update.html"
    success_url = reverse_lazy("users:users_list")

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления пользователя"""

    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("user:users_list")
    permission_required = "users.delete_user"
