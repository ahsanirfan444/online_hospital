from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from user_management import models

from user_management.serializer import CreateUserSerializer,GetUserSerializer


class CreateUser(APIView):

    def post(self, request, *args, **kwargs):
        user_serializer = CreateUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'error': [], 'error_code': '', 'data': user_serializer.validated_data, 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        else:

            return Response({'error': user_serializer.errors, 'error_code': '', 'data': [], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        


class GetUserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        user_obj = request.user

        user_serializer =GetUserSerializer(user_obj)

        return Response({'error': [], 'error_code': '', 'data': user_serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class AllPatientView(APIView):

    def get(self, request, *args, **kwargs):

        all_patients = models.User.objects.filter(is_active=True, user_type="P").exclude(is_superuser=True)

        user_serializer =GetUserSerializer(all_patients, many=True)

        return Response({'error': [], 'error_code': '', 'data': user_serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class AllCounsellortView(APIView):

    def get(self, request, *args, **kwargs):

        all_counsellors = models.User.objects.filter(is_active=True,user_type="C").exclude(is_superuser=True)

        user_serializer =GetUserSerializer(all_counsellors, many=True)

        return Response({'error': [], 'error_code': '', 'data': user_serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


