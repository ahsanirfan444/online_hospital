from rest_framework import serializers

from appointment_app import models
from user_management.models import User


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('patient','counsellor','date',)



   
class AppointmentsRecordSerializer(serializers.Serializer):
    start_date = serializers.DateField(allow_null=False,required=True)
    end_date = serializers.DateField(allow_null=False,required=True)
    
    def create(self, validated_data):
        return validated_data
    


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username','user_type',)


class GetAppointmentSerializer(serializers.ModelSerializer):
    patient = GetUserSerializer()
    counsellor = GetUserSerializer()
    class Meta:
        model = models.Appointment
        fields = ('patient','counsellor','date',)