from django.contrib import admin
from .models import *
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display=["has_cookie"]
    list_filter=["has_cookie"]

admin.site.register(Account, AccountAdmin)
admin.site.register(Site_Info)
admin.site.register(Contact)

