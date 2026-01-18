from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PositiveIntegerField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = PhoneNumberField(
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    number_snils = PositiveIntegerField(
        verbose_name="номер СНИЛС",
        null=True,
        blank=True,
        help_text="Введите номер СНИЛС",
    )
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Телеграм chat_id",
        null=True,
        blank=True,
        help_text="Введите телеграм chat_id",
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
