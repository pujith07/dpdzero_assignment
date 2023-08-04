from rest_framework import serializers
from api.models import *

class UserData_Serializer(serializers.ModelSerializer):
    class Meta:
        model=User_Data
        fields="__all__"

class Stored_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Stored_data
        fields="__all__"
        