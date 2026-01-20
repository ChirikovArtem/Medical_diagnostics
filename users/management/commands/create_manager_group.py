from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from organisation.models import Employee, Organisation, Record
from users.models import User


class Command(BaseCommand):
    """Кастомная команда для создания группы Менеджер управления данными организации, записями, сотрудниками"""

    def handle(self, *args, **kwargs):
        group_name = "Менеджер"
        group, created = Group.objects.get_or_create(name=group_name)

        permissions_list = []

        ct_organisation = ContentType.objects.get_for_model(Organisation)
        for perm_code in ["change", "add", "delete"]:
            perm_name = f"{perm_code}_organisation"
            try:
                perm = Permission.objects.get(
                    codename=perm_name, content_type=ct_organisation
                )
                permissions_list.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(f"Права {perm_name} не найдены.")

        # Модель User
        ct_user = ContentType.objects.get_for_model(User)
        for perm_code in ["change", "add", "delete"]:
            perm_name = f"{perm_code}_user"
            try:
                perm = Permission.objects.get(codename=perm_name, content_type=ct_user)
                permissions_list.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(f"Права {perm_name} не найдены.")

        # Модель Service
        ct_record = ContentType.objects.get_for_model(Record)
        for perm_code in ["change", "add", "delete"]:
            perm_name = f"{perm_code}_record"
            try:
                perm = Permission.objects.get(
                    codename=perm_name, content_type=ct_record
                )
                permissions_list.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(f"Права {perm_name} не найдены.")

        # Модель Employee
        ct_employee = ContentType.objects.get_for_model(Employee)
        for perm_code in ["change", "add", "delete"]:
            perm_name = f"{perm_code}_employee"
            try:
                perm = Permission.objects.get(
                    codename=perm_name, content_type=ct_employee
                )
                permissions_list.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(f"Права {perm_name} не найдены.")

        group.permissions.set(permissions_list)
        group.save()

        self.stdout.write(f'Группа "{group_name}" успешно создана с правами.')
