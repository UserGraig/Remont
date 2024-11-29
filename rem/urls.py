from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "rem"

router = routers.DefaultRouter()
router.register("masters", views.MasterViewSet)
router.register("clients", views.ClientViewSet)
router.register("specialisties", views.SpecialityViewSet)
router.register("orders", views.OrderViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]



