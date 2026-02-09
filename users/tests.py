import secrets

from django.test import Client, TestCase
from django.urls import reverse
from phonenumber_field.phonenumber import PhoneNumber

from users.models import User


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            phone=PhoneNumber.from_string("+79991234567"),
            city="Москва",
        )

        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )

    def test_register_user_success(self):
        """Успешная регистрация: пользователь создан, письмо отправлено, неактивен"""
        data = {
            "email": "new@example.com",
            "password1": "newpass123",
            "password2": "newpass123",
            "phone": "+79997654321",
            "city": "СПб",
        }
        response = self.client.post(reverse("users:user_form"), data)

        self.assertRedirects(response, reverse("users:login"))

        new_user = User.objects.get(email="new@example.com")
        self.assertFalse(new_user.is_active)
        self.assertIsNotNone(new_user.token)

    def test_register_user_invalid_email(self):
        """Ошибка при неверном email"""
        data = {"email": "invalid", "password1": "pass", "password2": "pass"}
        response = self.client.post(reverse("users:user_form"), data)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Enter a valid email address.",
            status_code=200,
        )

    def test_email_confirm_success(self):
        """Успешное подтверждение почты по токену"""
        token = secrets.token_hex(16)
        self.user.token = token
        self.user.save()

        response = self.client.get(
            reverse("users:email-confirm", kwargs={"token": token})
        )
        self.assertRedirects(response, reverse("users:login"))

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertIsNone(self.user.token)

    def test_email_confirm_invalid_token(self):
        """Ошибка при неверном токене"""
        response = self.client.get(
            reverse("users:email-confirm", kwargs={"token": "badtoken"})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_list_user_no_access(self):
        """Обычный пользователь не видит список"""
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse("users:users_list"))
        self.assertEqual(response.status_code, 403)

    def test_update_other_profile(self):
        """Нельзя редактировать чужой профиль"""
        self.client.login(email="test@example.com", password="password123")
        data = {"city": "Чужой город"}
        response = self.client.post(
            reverse("users:users_update", kwargs={"pk": self.admin.pk}), data
        )
        self.assertEqual(response.status_code, 404)
