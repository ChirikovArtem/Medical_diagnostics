from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import BooleanField

from users.models import User

def generate_time_choices(start_time_str="07:00", end_time_str="19:00", interval_minutes=30):
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")
    delta = timedelta(minutes=interval_minutes)
    choices = []

    current_time = start_time
    while current_time <= end_time:
        time_str = current_time.strftime("%H:%M")
        choices.append((time_str, time_str))
        current_time += delta

    return choices

class StyleFormMixin:
    """Стилизация форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

            if field_name == "phone":
                field.widget.attrs.update({"placeholder": "+7 (XXX) XXX-XX-XX"})
            if field_name == "number_snils":
                field.widget.attrs.update({"placeholder": "XXX-XXX-XXX XX"})
            if field_name == "date_registration":
                field.widget = forms.DateInput(
                    attrs={
                        "type": "date",
                        "class": "form-control datepicker",
                        "min": datetime.now().strftime("%Y-%m-%d"),
                    },
                    format="%Y-%m-%d",
                )
            if field_name == "time_registration":
                # Используйте выбранный подход — выбор фиксированных временных интервалов
                self.fields['time_registration'] = forms.ChoiceField(
                    choices=generate_time_choices(),
                    widget=forms.Select(attrs={
                        "class": "form-control",
                    })
                )


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""

    username = None

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "tg_chat_id",
            "city",
            "number_snils",
            "password1",
            "password2",
        )


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    """Форма изменения профиля пользователя"""

    username = None

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "tg_chat_id",
            "city",
            "number_snils",
        )
