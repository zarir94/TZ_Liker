import schedule
from time import sleep

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

schedule.every().hours.do(check_cookie)

def run_task():
	while True:
		schedule.run_pending()
		sleep(int(60*15)) # Sleep 15 minutes

		
