from django.apps import AppConfig
from threading import Thread
from .schedules import schedules

def add_to_liker_thread():
	from Home.views import add_auto_submit_thread
	from Home.models import Liker_Threads_Info
	for info in Liker_Threads_Info.objects.all():
		add_auto_submit_thread(info.react, info.post_id, info.user, info.amount)

class HomeConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'Home'

	def ready(self):
		t=Thread(target=schedules.run_task)
		t.setDaemon(True)
		t.start()
		t2=Thread(target=add_to_liker_thread)
		t2.setDaemon(True)
		t2.start()

