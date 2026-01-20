from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from organisation.forms import EmployeeForm, OrganisationForm, RecordForm
from organisation.models import Employee, Organisation, Record


class HomeViews(TemplateView):
    """Контроллер для отображения главной страница сайта"""

    model = Organisation
    template_name = "organisation/home.html"
    success_url = reverse_lazy("organisation:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation"] = Organisation.objects.get(id=1)
        return context


class AboutOrganisationViews(TemplateView):
    """Контроллер для отображения страницы о медицинской организации"""

    model = Organisation
    template_name = "organisation/organisation.html"

    def get_context_data(self, **kwargs):
        """Отправка формы в шаблон"""
        context = super().get_context_data(**kwargs)
        context["organisation"] = Organisation.objects.get(id=1)
        context["employees"] = Employee.objects.all()
        return context


class ServicesViews(TemplateView):
    """Контроллер для отображения страницы услуги"""

    model = Record
    template_name = "organisation/services.html"


class ContactsViews(TemplateView):
    """Контроллер для отображения страницы контакты"""

    model = Organisation
    template_name = "organisation/contacts.html"


class FeedbackViews(TemplateView):
    """Контроллер для отображения страницы обратной связи"""

    model = Organisation
    template_name = "organisation/feedback.html"


def feedback_submit(request):
    """Отправка письма обратной связи"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"Обратная связь от {name}"
        message_body = f"Имя: {name}\nEmail: {email}\n\nСообщение:\n{message}"
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            messages.success(request, "Ваш отзыв отправлен. Спасибо!")
        except Exception as e:
            messages.error(request, "Ошибка при отправке письма. Попробуйте позже.")

        return redirect("organisation:feedback")
    else:
        return redirect("organisation:feedback")


class SiteManagementViews(TemplateView):
    """Контроллер для отображения страниц редактирования сайта"""

    model = Organisation
    template_name = "organisation/site_management.html"

    def get_context_data(self, **kwargs):
        """Отправка формы в шаблон"""
        context = super().get_context_data(**kwargs)
        context["organisation"] = Organisation.objects.get(id=1)
        context["employees"] = Employee.objects.all()
        context["record"] = Record.objects.all()
        return context


class OrganisationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер изменения информации о медицинской организации"""

    model = Organisation
    form_class = OrganisationForm
    template_name = "organisation/organisation_form.html"
    success_url = reverse_lazy("organisation:home")
    permission_required = "organisation.change_organisation"


class EmployeeDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Контроллер детализации сотрудника"""

    model = Employee
    template_name = "organisation/employee_detail.html"
    context_object_name = "employee"
    permission_required = "organisation.view_employee"


class EmployeeList(ListView):
    """Контроллер вывода списка сотрудников"""

    model = Employee
    template_name = "organisation/employee_list.html"
    context_object_name = "employees"


class EmployeeCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер создания нового сотрудника"""

    model = Employee
    form_class = EmployeeForm
    template_name = "organisation/employee_form.html"
    success_url = reverse_lazy("organisation:employee_list")
    permission_required = "organisation.add_employee"


class EmployeeDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления сотрудников"""

    model = Employee
    template_name = "organisation/employee_delete.html"
    success_url = reverse_lazy("organisation:employee_list")
    context_object_name = "employee"
    permission_required = "organisation.delete_employee"


class EmployeeUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер изменения сотрудников"""

    model = Employee
    form_class = EmployeeForm
    template_name = "organisation/employee_form.html"
    success_url = reverse_lazy("organisation:employee_list")
    permission_required = "organisation.change_employee"


class RecordDetail(DetailView):
    """Контроллер детализации услуги"""

    model = Record
    template_name = "record/record_detail.html"
    context_object_name = "record"


class RecordList(ListView):
    """Контроллер вывода списка услуг"""

    model = Record
    template_name = "record/record_list.html"
    context_object_name = "records"


class RecordCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер создания новой услуги"""

    model = Record
    form_class = RecordForm
    template_name = "record/record_form.html"
    success_url = reverse_lazy("organisation:record_list")
    permission_required = "organisation.add_record"


class RecordDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления услуги"""

    model = Record
    template_name = "record/record_delete.html"
    success_url = reverse_lazy("organisation:record_list")
    context_object_name = "record"
    permission_required = "organisation.delete_record"


class RecordUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер изменения услуги"""

    model = Record
    form_class = RecordForm
    template_name = "record/record_form.html"
    success_url = reverse_lazy("organisation:record_list")
    permission_required = "organisation.change_record"
