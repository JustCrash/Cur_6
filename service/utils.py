from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
from service.models import Mailing, Attempt
from config import settings

import pytz
import smtplib


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(time_sending=current_datetime, status=Mailing.status_chose)

    for mailing in mailings:
        last_attempt = Attempt.objects.filter(mailing=mailing).order_by('-attempt_date').first()
        next_send_time = current_datetime

        if mailing.time_sending <= current_datetime:
            server_response = send_mail(
                subject=title,
                message=content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email for recipient in mailing.recipients.all()],
                fail_silently=False,
            )
            if server_response == 1:
                server_response = 'Письмо успешно отправлено'
            Attempt.objects.create(status='success', answer=server_response, mailing=mailing)

            if mailing.periodicity == Mailing.DAILY:
                next_send_time = last_attempt.attempt_date + timedelta(days=1) if last_attempt else current_datetime
            elif mailing.periodicity == Mailing.WEEKLY:
                next_send_time = last_attempt.attempt_date + timedelta(weeks=1) if last_attempt else current_datetime
            elif mailing.periodicity == Mailing.MONTHLY:
                next_send_time = last_attempt.attempt_date + timedelta(weeks=4) if last_attempt else current_datetime

            if current_datetime >= next_send_time:
                send_email(mailing.message.subject, mailing.message.body, [clients.email for clients in mailing.clients.all()])
                Attempt.objects.create(newsletter=mailing, attempt_date=current_datetime)
