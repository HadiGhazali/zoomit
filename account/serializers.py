from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'last_name', 'is_staff', 'is_active', 'id', 'get_full_name']

# class UserSerializer2(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     full_name = serializers.CharField(max_length=150)
#
#     def create(self, validated_data):
#         pass
#
#     def validate(self, email):
#         pass
