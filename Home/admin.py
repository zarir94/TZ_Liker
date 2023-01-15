from django.contrib import admin
from .models import *
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display=["username","email","has_cookie"]
    list_filter=["has_cookie"]

admin.site.register(Account, AccountAdmin)
admin.site.register(Site_Info)
admin.site.register(Contact)
admin.site.register(Liker_Threads_Info)

