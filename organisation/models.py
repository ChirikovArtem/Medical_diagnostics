from django.db import models


class Organisation(models.Model):
    """Модель организация"""

    name = models.CharField(
        max_length=200, verbose_name="Название организации медицинской диагностики"
    )
    logo = models.ImageField(
        upload_to="photos/",
        verbose_name="Логотип организации медицинской диагностики",
        blank=True,
        null=True,
    )
    story = models.TextField(verbose_name="История организации", null=True, blank=True)
    mission = models.TextField(verbose_name="Миссия", null=True, blank=True)
    values = models.TextField(verbose_name="Ценности", null=True, blank=True)
    description = models.TextField(
        verbose_name="Описание организации", null=True, blank=True
    )

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"


class Employee(models.Model):
    """Модель сотрудники организации медицинской диагностики"""

    first_name = models.CharField(max_length=200, verbose_name="Имя сотрудника")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия сотрудника")
    photo_employee = models.ImageField(
        upload_to="photos/", verbose_name="Фото сотрудника"
    )
    job_title = models.CharField(max_length=200, verbose_name="Должность")
    specialization = models.TextField(
        max_length=50, verbose_name="Специализация", null=True, blank=True
    )
    work_experience = models.CharField(
        max_length=50, verbose_name="Стаж работы", null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"


class Record(models.Model):
    """Модель услуги для записи"""

    LABSTUDY_RECORD = "Лабораторные исследования"
    THERAPEVT_RECORD = "Терапевт"
    UZI_RECORD = "УЗИ"
    FUNCZIONAL_RECORD = "Функциональная диагностика"

    CHOOSING_SPECIALIST = [
        (LABSTUDY_RECORD, "Лабораторные исследования"),
        (THERAPEVT_RECORD, "Терапевт"),
        (UZI_RECORD, "УЗИ"),
        (FUNCZIONAL_RECORD, "Функциональная диагностика"),
    ]

    service = models.CharField(
        max_length=200,
        choices=CHOOSING_SPECIALIST,
        default=THERAPEVT_RECORD,
        verbose_name="Оказываемая услуга",
        help_text="Укажите услугу",
    )
    cabinet_number = models.PositiveIntegerField(
        unique=True, verbose_name="Номер кабинета"
    )
    doctor = models.ForeignKey(
        Employee,
        verbose_name="Специалист",
        on_delete=models.CASCADE,
        related_name="doctor",
    )
    description_service = models.TextField(
        verbose_name="Описание услуги", null=True, blank=True
    )

    def __str__(self):
        return (
            f"Терапевт проводится в кабинете №{self.cabinet_number}. "
            f"Специалист - {self.doctor.first_name} {self.doctor.last_name}"
        )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
