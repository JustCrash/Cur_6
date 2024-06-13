from django.conf import settings
from datetime import datetime
import pytz


def mailings():
    time_zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(time_zone)
    print(f'Current time: {now}')