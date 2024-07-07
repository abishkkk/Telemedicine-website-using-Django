from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registeration/', views.registeration, name='registeration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('doctors/', views.doctors_list, name='doctor_list'),
    path('patients/', views.patients_list, name='patients_list'),
