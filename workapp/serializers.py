from rest_framework import serializers
from .models import Add_edit_del_date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import CustomUser

User = get_user_model()



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_edit_del_date
        fields = ["id",'task','description','user']