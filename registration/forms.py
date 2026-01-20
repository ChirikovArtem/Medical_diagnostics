import logging
from datetime import date, datetime, time

from django import forms
from django.core.exceptions import ValidationError

from registration.models import Registration
from users.forms import StyleFormMixin


class RegistrationForm(StyleFormMixin, forms.ModelForm):
    """Форма для записи на услугу"""

    class Meta:
        model = Registration
        exclude = ("patient",)

    def clean_date_registration(self):
        """Валидация даты бронирования"""
        date_registration = self.cleaned_data.get("date_registration")
        today = date.today()

        if date_registration <= today:
            raise ValidationError("Дата записи не может быть раньше сегодняшнего дня")

        if date_registration.isoweekday() == 7:
            raise ValidationError("Выходной день")

        return date_registration

    def clean(self):
        logger = logging.getLogger()
        time_registration_str = self.cleaned_data.get("time_registration")
        logger.info(time_registration_str)

    def clean_time_registration(self):
        """Валидация времени записи"""
        logger = logging.getLogger()
        time_registration_str = self.cleaned_data.get("time_registration")
        logger.info(time_registration_str)
        if time_registration_str is None:
            return time_registration_str

        # Преобразуем строку в объект time
        try:
            time_registration_obj = datetime.strptime(
                time_registration_str, "%H:%M"
            ).time()
        except ValueError:
            raise ValidationError(
                "Некорректный формат времени. Используйте формат HH:MM."
            )

        # Проверка интервала
        if time_registration_obj < time(7, 0) or time_registration_obj > time(19, 0):
            raise ValidationError(
                "Время записи должно быть в диапазоне с 07:00 до 19:00"
            )
        if time_registration_obj <= datetime.now().time():
            raise ValidationError("Время записи должно быть не раньше текущего времени")
        return time_registration_str
