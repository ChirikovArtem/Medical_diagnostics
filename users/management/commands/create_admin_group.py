from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from registration.models import Registration


class Command(BaseCommand):
    """Кастомная команда для создания группы Администратор для управления записями"""

    def handle(self, *args, **kwargs):
        group_name = "Администратор"
        group, created = Group.objects.get_or_create(name=group_name)

        permissions_list = []

        ct_registration = ContentType.objects.get_for_model(Registration)
        for perm_code in ["view", "add", "change", "delete"]:
            perm_name = f"{perm_code}_registration"
            try:
                perm = Permission.objects.get(
                    codename=perm_name, content_type=ct_registration
                )
                permissions_list.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(f"Права {perm_name} не найдены.")

        group.permissions.set(permissions_list)
        group.save()

        self.stdout.write(f'Группа "{group_name}" успешно создана и настроена.')
