import schedule
from time import sleep
from datetime import timedelta
from django.utils import timezone

def check_cookie():
	from Home.models import Account
	from Home.liker_helper import get_profile_id
	all_acc=Account.objects.filter(has_cookie=True)
	print('running')
	for acc in all_acc:
		profile_id=get_profile_id('https://www.facebook.com/4', acc.cookie)
		if not profile_id:
			acc.cookie=None
			acc.profile_id=None
			acc.has_cookie=False
			acc.save()

def delete_expired_thread():
	from Home.models import Liker_Threads_Info
	expiration_date = timezone.now() - timedelta(days=30)
	Liker_Threads_Info.objects.filter(created_at__lt=expiration_date).delete()

schedule.every().hours.do(check_cookie)
schedule.every().hours.do(delete_expired_thread)

def run_task():
	while True:
		schedule.run_pending()
		sleep(int(60*15)) # Sleep 15 minutes

		
