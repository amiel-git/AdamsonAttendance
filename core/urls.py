from django.urls import path 
from core import views

app_name = 'core'

urlpatterns = [
    path('',views.index,name='index'),
    path('registration/',views.registrationPage,name='registration'),
    path('login/',views.loginView,name="login"),
    path('logout/',views.logoutView,name="logout"),
]