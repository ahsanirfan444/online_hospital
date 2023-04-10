from django.urls import path, include
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter
from appointment_app import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create_appointment', views.AppointmentView)

urlpatterns = [

    path('', include(router.urls)),
    path('all_appointments/', views.ViewAppointmentAPI.as_view(), name='all_appointments'),
    path('all_appointments_patient/<int:pk>/', views.ViewAppointmentAPIForPatient.as_view(), name='all_appointments'),
    path('all_appointments_counsellor/<int:pk>/', views.ViewAppointmentAPIForCounsellor.as_view(), name='all_appointments'),
]

