"""
Этот файл содержит маршруты приложения для API.
"""

from django.urls import path, include
from rest_framework import routers
from rem import views  # Замените 'app_name' на название вашего приложения

APP_NAME = "rem"

router = routers.DefaultRouter()
router.register("masters", views.MasterViewSet)
router.register("clients", views.ClientViewSet)
router.register("specialisties", views.SpecialityViewSet)
router.register("orders", views.OrderViewSet)
router.register("services", views.ServiceViewSet)
router.register("reviews", views.ReviewViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
