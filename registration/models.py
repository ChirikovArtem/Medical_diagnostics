from django.db import models

from organisation.models import Record
from users.models import User


class Registration(models.Model):
    """Модель записи на услугу"""

    date_registration = models.DateField(
        verbose_name="Дата записи на услугу",
        help_text="Выберите число, на которое хотите записаться",
    )
    time_registration = models.TimeField(
        verbose_name="Время записи на услугу",
        help_text="Выберите время, на которое хотите записаться",
    )
    patient = models.ForeignKey(
        User,
        verbose_name="Пациент",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="registration_patient",
    )
    registration = models.ForeignKey(
        Record,
        verbose_name="Услуга",
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    def __str__(self):
        return (
            f"Пациент {self.patient} записался на {self.registration} "
            f"Дата: {self.date_registration} время: {self.time_registration}"
        )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
