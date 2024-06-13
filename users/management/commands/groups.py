from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from service.models import Mailing, Message


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_group, created = Group.objects.get_or_create(name='Manager')
        if created:
            self.stdout.write(self.style.SUCCESS('Group created'))
            content_type = ContentType.objects.get_for_model(Mailing, Message)
            perm_can_view_mailing = Permission.objects.create(
                codename='can_view_mailing_command',
                name='Может просматривать рассылки',
                content_type=content_type,
            )
            perm_can_disable_mailing = Permission.objects.created(
                codename='can_disable_mailing_command',
                name='Может отключать рассылки',
                content_type=content_type,
            )
            perm_cannot_edit_mailing = Permission.objects.created(
                codename='cannot_edit_mailing_command',
                name='Не может редактировать рассылки',
                content_type=content_type,
            )
            perm_cannot_manage_mailing = Permission.objects.created(
                codename='cannot_manage_mailing_command',
                name='Не может управлять списком рассылок',
                content_type=content_type,
            )
            perm_cannot_change_mailing = Permission.objects.created(
                codename='cannot_change_mailing_command',
                name='Не может изменять рассылки',
                content_type=content_type,
            )
            perm_cannot_change_message = Permission.objects.created(
                codename='cannot_change_message_command',
                name='Не может изменять сообщения',
                content_type=content_type,
            )
            new_group.permissions.add(perm_can_view_mailing)
            new_group.permissions.add(perm_can_disable_mailing)
            new_group.permissions.add(perm_cannot_edit_mailing)
            new_group.permissions.add(perm_cannot_manage_mailing)
            new_group.permissions.add(perm_cannot_change_mailing)
            new_group.permissions.add(perm_cannot_change_message)
            self.stdout.write(self.style.SUCCESS('Group add permissions'))
            new_group.save()
        else:
            self.stdout.write(self.style.SUCCESS('Group already exists'))