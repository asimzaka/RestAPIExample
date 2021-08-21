from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from restapi import serializers
from restapi.models import Task

class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user:
            response = {
                "user": {"id": request.user.id, "email": request.user.email}
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

class CreateUserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = serializers.RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerelizer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    http_method_names = ['post', 'get']

    def create(self, request, *args, **kwargs):
        task_data = JSONParser().parse(request)
        task_serializer = serializers.TaskSerelizer(data=task_data)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse({"task": task_serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)