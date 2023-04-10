from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    path("user/", include("user_management.urls")),
    path("appointment/", include("appointment_app.urls")),
]
