"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')
router.register(r'leaderboards', views.LeaderboardViewSet, basename='leaderboard')

# Helper to get the codespace API base URL
def get_api_base_url(request):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        # Use HTTPS for codespace public URL
        return f"https://{codespace_name}-8000.app.github.dev/api/"
    # Fallback to localhost for local dev
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    return f"{scheme}://{host}/api/"

# Custom API root view to return API endpoints with correct base URL
from rest_framework.decorators import api_view
@api_view(['GET'])
def custom_api_root(request, format=None):
    base_url = get_api_base_url(request)
    return JsonResponse({
        'users': base_url + 'users/',
        'teams': base_url + 'teams/',
        'activities': base_url + 'activities/',
        'workouts': base_url + 'workouts/',
        'leaderboards': base_url + 'leaderboards/',
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', custom_api_root, name='api-root'),
    path('api/', include(router.urls)),
]
