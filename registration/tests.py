from datetime import date, datetime, time, timedelta
from unittest.mock import patch

from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse

from organisation.models import Employee, Record
from registration.forms import RegistrationForm
from registration.models import Registration
from registration.services import get_free_records
from users.models import User


class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            phone="+79991234567",
            city="Москва",
        )
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="password123",
            phone="+79997654321",
            city="Санкт-Петербург",
        )
        admin_group = Group.objects.create(name="Администратор")
        self.admin_user.groups.add(admin_group)

        self.employee = Employee.objects.create(
            first_name="Иван",
            last_name="Иванов",
            job_title="Терапевт",
            photo_employee="photos/test.jpg",
        )
        self.record = Record.objects.create(
            service=Record.THERAPEVT_RECORD,
            cabinet_number=101,
            doctor=self.employee,
            description_service="Приём терапевта",
        )

    def test_record_str(self):
        expected = "Терапевт проводится в кабинете №101. Специалист - Иван Иванов"
        self.assertEqual(str(self.record), expected)

    def test_registration_str(self):
        registration = Registration.objects.create(
            date_registration=date(2026, 2, 1),
            time_registration=time(10, 0),
            patient=self.user,
            registration=self.record,
        )
        expected = (
            "Пациент test@example.com записался на Терапевт проводится в кабинете №101. "
            "Специалист - Иван Иванов Дата: 2026-02-01 время: 10:00:00"
        )
        self.assertEqual(str(registration), expected)

    def test_user_str(self):
        self.assertEqual(str(self.user), "test@example.com")


class ServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.employee = Employee.objects.create(
            first_name="Анна", last_name="Петрова", job_title="УЗИст"
        )
        self.record1 = Record.objects.create(
            service=Record.UZI_RECORD, cabinet_number=202, doctor=self.employee
        )
        self.record2 = Record.objects.create(
            service=Record.LABSTUDY_RECORD, cabinet_number=303, doctor=self.employee
        )

    def test_get_free_records_past_time(self):
        past_date = date(2025, 12, 1)
        past_time = time(9, 0)
        result = get_free_records(past_date, past_time)
        self.assertEqual(result.count(), 0)

    def test_get_free_records_no_conflicts(self):
        future_date = date(2026, 3, 1)
        future_time = time(14, 0)
        result = get_free_records(future_date, future_time)
        self.assertQuerySetEqual(result, [self.record1, self.record2], ordered=False)

    def test_get_free_records_with_conflict(self):
        Registration.objects.create(
            date_registration=date(2026, 3, 1),
            time_registration=time(14, 0),
            patient=self.user,
            registration=self.record1,
        )
        result = get_free_records(date(2026, 3, 1), time(14, 0))
        self.assertQuerySetEqual(result, [self.record2])


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.admin_user = User.objects.create_user(
            email="admin@example.com", password="password123"
        )
        admin_group = Group.objects.create(name="Администратор")
        self.admin_user.groups.add(admin_group)

        self.employee = Employee.objects.create(
            first_name="Ольга", last_name="Сидорова", job_title="Лаборант"
        )
        self.record = Record.objects.create(
            service=Record.LABSTUDY_RECORD, cabinet_number=404, doctor=self.employee
        )

    def test_registration_create_get(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse("registration:registration_form"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertContains(response, "date_registration")
        self.assertContains(response, "time_registration")


class TestRegistrationFormBasic(TestCase):

    def setUp(self):
        self.test_record = Record.objects.create(
            service=Record.THERAPEVT_RECORD,
            cabinet_number=999,
            doctor=Employee.objects.create(
                first_name="Тест", last_name="Доктор", job_title="Терапевт"
            ),
        )
        self.valid_time = "10:00"

    def test_past_date(self):
        form = RegistrationForm(
            data={
                "date_registration": date.today() - timedelta(days=1),
                "time_registration": self.valid_time,
                "registration": self.test_record.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("date_registration", form.errors)


def test_sunday_date(self):
    today = date.today()
    days_ahead = 6 - today.isoweekday()  # до воскресенья
    if days_ahead < 0:
        days_ahead += 7
    sunday = today + timedelta(days=days_ahead)

    form = RegistrationForm(
        data={
            "date_registration": sunday,
            "time_registration": self.valid_time,
            "registration": self.test_record.pk,
        }
    )
    self.assertFalse(form.is_valid())
    self.assertTrue(
        "date_registration" in form.errors or "time_registration" in form.errors,
        f"Ожидалась ошибка в date_registration или time_registration, но ошибок нет: {form.errors}",
    )


def test_invalid_time_format(self):
    form = RegistrationForm(
        data={
            "date_registration": date.today() + timedelta(days=1),
            "time_registration": "12.30",  # точка вместо :
            "registration": self.test_record.pk,
        }
    )
    self.assertFalse(form.is_valid())
    self.assertIn("time_registration", form.errors)


def test_time_out_of_range(self):
    form = RegistrationForm(
        data={
            "date_registration": date.today() + timedelta(days=1),
            "time_registration": "20:00",
            "registration": self.test_record.pk,
        }
    )
    self.assertFalse(form.is_valid())
    self.assertIn("time_registration", form.errors)


@patch("datetime.datetime")
def test_time_before_now(self, mock_datetime):
    mock_datetime.now.return_value = datetime.combine(date.today(), time(15, 0))

    form = RegistrationForm(
        data={
            "date_registration": date.today(),
            "time_registration": "14:00",  # раньше 15:00
            "registration": self.test_record.pk,
        }
    )
    self.assertFalse(form.is_valid())
    self.assertIn("time_registration", form.errors)
