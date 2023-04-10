from django.urls import path, include
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter

from user_management.views import CreateUser, GetUserDetails,AllPatientView,AllCounsellortView



urlpatterns = [
    
path('create_user/', CreateUser.as_view(), name='create_user'),
path('details/', GetUserDetails.as_view(), name='create_user'),
path('all_patient/', AllPatientView.as_view(), name='all_patient'),
path('all_counsellor/', AllCounsellortView.as_view(), name='all_patient'),
]
