from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreationTest(TestCase):
    def setUp(self):
        # Создаём пользователя перед тестами
        self.user = User(
            email='testuser@example.com',
            city='Москва',
            phone='+79991234567',
        )
        self.user.set_password('my_secure_password')
        self.user.save()

    def test_user_creation(self):
        # Проверяем, что пользователь создан и правильно сохранён
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.city, 'Москва')
        self.assertTrue(user.check_password('my_secure_password'))
        self.assertIsNotNone(user.id)

    def test_user_str(self):
        # Проверка метода __str__
        self.assertEqual(str(self.user), 'testuser@example.com')


