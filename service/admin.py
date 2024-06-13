from django.contrib import admin


from service.models import Client, Mailing, Message, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'email']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'time_sending', 'periodicity', 'status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'subject']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status']
