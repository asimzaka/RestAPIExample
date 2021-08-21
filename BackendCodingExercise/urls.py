"""BackendCodingExercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from restapi import views
from rest_framework_simplejwt import views as jwt_views
from restapi.serializers import JWTSerializer

task_list = views.TaskView.as_view({
    'get': 'list',
})
task_create = views.TaskView.as_view({
    'post': 'create',
})

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/create-task/', task_create),
    path('api/list-tasks/', task_list),
    path('api/register/',  views.CreateUserViewSet.as_view(), name='Register'),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(serializer_class=JWTSerializer), name='token_obtain_pair'),
    path('api/user/',  views.UserViewSet.as_view(), name='User List'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
