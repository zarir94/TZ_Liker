from django.views.generic.base import RedirectView
from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('login/', login),
    path('logout/', logout),
    path('delete/', delete),
    path('register/', register),
    path('reset-password/', reset_password),
    path('change-password/', change_password),
    path('switchtheme/', switch_theme),
    path('verify/', verify_email),
    path('about/', about),
    path('contact/', contact),
    path('tutorial/', tutorial),
    path('inspector-apk/', inspector_apk),
    path('dashboard/', dashboard),
    path('settings/', settings),
    path('dashboard/rapid-like/', rapid_like),
    path('dashboard/auto-like/', auto_like),
    path('dashboard/auto-follow/', auto_follow),
    path('googled3920a951d8fb79c.html', google_verify),
    path('favicon.ico', RedirectView.as_view(url='https://technicalzarir.blogspot.com/favicon.ico')),
]
