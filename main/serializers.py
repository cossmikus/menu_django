from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserSerializerNames(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
        

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = The_Admin
        fields = '__all__'
class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = The_Trainer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = The_Client
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'