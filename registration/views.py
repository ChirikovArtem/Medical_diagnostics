from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from organisation.models import Record
from registration.forms import RegistrationForm
from registration.models import Registration
from registration.services import get_free_records


class RegistrationCreate(LoginRequiredMixin, CreateView):
    """Контроллер новой записи"""

    model = Registration
    form_class = RegistrationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("registration:personal_account")

    def form_valid(self, form):
        # Проверка наличия уже существующей записи
        date = form.cleaned_data["date_registration"]
        time = form.cleaned_data["time_registration"]
        registration_obj = form.cleaned_data["registration"]
        user = self.request.user

        # Используем правильное имя поля для фильтрации
        exists = Registration.objects.filter(
            date_registration=date,
            time_registration=time,
            registration=registration_obj,
        ).exists()

        if exists:
            form.add_error(None, "Данное время уже занято.")
            return self.form_invalid(form)

        registration = form.save()
        registration.patient = user
        registration.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Отправка формы в шаблон"""
        context = super().get_context_data(**kwargs)
        context["all_records"] = Record.objects.all()
        return context


@require_GET
def get_available_records(request):
    """AJAX-функция для получения доступных записей"""
    date_str = request.GET.get("date_registration")
    time_str = request.GET.get("time_registration")

    if not date_str or not time_str:
        return JsonResponse({"error": "Не указана дата или время"}, status=400)
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
        available_services = get_free_records(date, time)
        services_data = [
            {
                "id": service.id,
                "service": service.service,
                "cabinet_number": service.cabinet_number,
                "doctor": str(service.doctor),
                "description": service.description_service or "",
            }
            for service in available_services
        ]

        return JsonResponse(services_data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


class RegistrationDetail(LoginRequiredMixin, DetailView):
    """Контроллер просмотра"""

    model = Registration
    template_name = "registration/registration_detail.html"


class RegistrationList(LoginRequiredMixin, ListView):
    """Контроллер просмотра всех бронирований"""

    model = Registration
    template_name = "registration/registration_list.html"
    context_object_name = "registrations"
    ordering = ["-date_registration", "-time_registration"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="Администратор").exists():
            return queryset
        else:
            return queryset.filter(patient=user)


class RegistrationDelete(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления бронирования"""

    model = Registration
    template_name = "registration/registration_delete.html"
    success_url = reverse_lazy("registration:registration_list")


class RegistrationUpdate(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования бронирования"""

    model = Registration
    form_class = RegistrationForm
    template_name = "registration/registration_form.html"

    def get_success_url(self):
        return reverse("registration:registration_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        """Отправка формы в шаблон"""
        context = super().get_context_data(**kwargs)
        context["all_records"] = Record.objects.all()
        context["today_record"] = date.today().isoformat()
        return context


class PersonalAccountViews(LoginRequiredMixin, TemplateView):
    """Контроллер для отображения личного кабинета пользователя"""

    model = Registration
    template_name = "registration/personal_account.html"

    def get_context_data(self, **kwargs):
        """Отправка формы в шаблон"""
        context = super().get_context_data(**kwargs)
        now = timezone.now().date()

        all_registrations = Registration.objects.filter(patient=self.request.user)
        context["bookings_history"] = all_registrations.filter(
            date_registration__lt=now
        ).order_by("-date_registration")
        context["current_bookings"] = all_registrations.filter(
            date_registration__gte=now
        ).order_by("date_registration")

        return context
