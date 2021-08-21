from django.contrib.auth.models import User, Group
from .models import Task
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, data):
        user = User.objects.create(
            email=data['email'],
            username=data['email'],
        )
        user.set_password(data['password'])
        user.save()

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TaskSerelizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name']


class JWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)