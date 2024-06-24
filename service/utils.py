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

    mailings = Mailing.objects.filter(time_sending=current_datetime).filter(
        status=['created', 'launched'])

    for mailing in mailings:
        if mailing.time_sending is None:
            mailing.time_sending = current_datetime
        title = mailing.message.subject
        content = mailing.message.text
        mailing.status = 'launched'
        mailing.save()

        try:
            if mailing.time_end < mailing.time_sending:
                mailing.time_sending = current_datetime
                mailing.status = 'completed'
                mailing.save()
                continue

            if mailing.time_sending <= current_datetime:
                server_response = send_mail(
                    subject=title,
                    message=content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email for recipient in mailing.clients.all()],
                    fail_silently=False,
                )
                if server_response == 1:
                    server_response = 'Письмо успешно отправлено'
                Attempt.objects.create(status='successful', answer=server_response, mailing=mailing)

                if mailing.periodicity == 'everyday':
                    miling.time_sending = current_datetime + timedelta(days=1)
                elif mailing.periodicity == 'once a week':
                    miling.time_sending = current_datetime + timedelta(days=7)
                elif mailing.periodicity == 'один раз в месяц':
                    miling.time_sending = current_datetime + timedelta(months=1)

        except smtplib.SMTPException as error:
            Attempt.objects.create(status='unsuccessful', answer=error, mailing=mailing)
