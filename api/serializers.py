# file to verify and convert models into json format

# import serializers
from rest_framework import serializers

# import models
from .models import User

# creating a serializer:
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # define the base model
        fields = '__all__'              # get all fields from this model
        # fields = ['id', 'field1']     # can select just some of the models