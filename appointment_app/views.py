import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from appointment_app import models
from appointment_app.serializer import AppointmentSerializer,AppointmentsRecordSerializer,GetAppointmentSerializer


 
class AppointmentView(viewsets.ModelViewSet):

    serializer_class = AppointmentSerializer
    queryset = models.Appointment.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        validation = serializer.is_valid()

        if validation:
            self.perform_create(serializer)

            returnObj = serializer.data
           

            return Response({'error': [], 'error_code': '', 'data': [returnObj], 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)


        return Response({'error': serializer.errors, 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):

        if models.Appointment.objects.filter(patient=serializer.validated_data['patient'],counsellor=serializer.validated_data['counsellor'],date=serializer.validated_data['date']).exists():
            raise serializers.ValidationError(
                {"appointment": "Your appointment is already booked with this counsellor on "+ str(serializer.validated_data['date'])})

        else:
            serializer.save()

    
class ViewAppointmentAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AppointmentsRecordSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            all_appointments =models.Appointment.objects.filter(is_active=True, date__range=(start_date, end_date)).order_by('-id')

            appointment_serializer = GetAppointmentSerializer(all_appointments, many=True)
            if appointment_serializer:
                return Response({'error': [], 'error_code': '', 'data': appointment_serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [serializer.errors], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        


class ViewAppointmentAPIForPatient(APIView):
    def get(self, request,pk, *args, **kwargs):
        if pk != None:
            all_appointments = models.Appointment.objects.filter(is_active=True, patient=pk).order_by('-id')

            appointment_serializer = GetAppointmentSerializer(all_appointments, many=True)
            if appointment_serializer:
                return Response({'error': [], 'error_code': '', 'data': appointment_serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No Patient"], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        

class ViewAppointmentAPIForCounsellor(APIView):
    def get(self, request,pk, *args, **kwargs):
        if pk != None:
            all_appointments = models.Appointment.objects.filter(is_active=True, counsellor=pk).order_by('-id')

            appointment_serializer = GetAppointmentSerializer(all_appointments, many=True)
            if appointment_serializer:
                return Response({'error': [], 'error_code': '', 'data': appointment_serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ["No Patient"], 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)