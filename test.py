

from datetime import timedelta
from django.utils import timezone
from Home.models import Liker_Threads_Info
import pytz

expiration_date = timezone.now() - timedelta(days=30)

print(expiration_date)
# Liker_Threads_Info.objects.filter(created_at__lt=expiration_date).delete()
