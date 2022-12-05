from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
	id = serializers.IntegerField(read_only=True)

	class Meta:
		model = User
		fields = '__all__'

	def create(self, validated_data):
		user = User.objects.create(**validated_data)
		user.set_password(user.password)
		user.save()
		return user


class CurrentUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ['password']
