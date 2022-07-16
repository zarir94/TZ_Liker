from django.apps import AppConfig
from threading import Thread
from .schedules import schedules

class HomeConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'Home'

	def ready(self):
		t=Thread(target=schedules.run_task)
		t.setDaemon(True)
		t.start()

