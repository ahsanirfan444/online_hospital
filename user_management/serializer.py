from rest_framework import serializers
from user_management import models
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
        

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id','first_name', 'last_name', 'email','username','user_type',)

    
    def to_representation(self, instance):

        response = super().to_representation(instance)
        if response['user_type'] == 'P':
            response['user_type'] = "Patient"
        else:
            response['user_type'] = "Counsellor"
        return response


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name','last_name','email','user_type','password','username')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        models.User.objects.create_user(**validated_data)        
        return validated_data
        



    def validate(self, data):
        user_obj = models.User.objects.filter(username=data['username'])
        if user_obj:
            raise serializers.ValidationError('Already exist')
        else:
            user_obj = models.User.objects.filter(email=data['email'],user_type= data['user_type'])
            if user_obj:
                raise serializers.ValidationError({"user_type":"User already created for this user type"})
            else:
                return super().validate(data)

                

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value


    def validate_user_type(self, value):
        if value == "C" or value == "P":
            return value
        else:
            raise serializers.ValidationError('Not a valid user type')
        



class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = models.User.objects.filter(email = data['email']).exists()
        if user:
            user = models.User.objects.get(email = data['email'])
            if user.check_password(data['password']):
                return super(EmailLoginSerializer, self).validate(data)
            
            else:
                raise serializers.ValidationError({"password":"Incorrect Password"})
        else:
            raise serializers.ValidationError("No user Exist !")
        