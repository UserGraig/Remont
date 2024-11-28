import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import Client, Order, Speciality, Master
from .serializers import ClientSerializer, SpecialitySerializer, OrderSerializer, MasterSerializer

# Create your views here.

class OrderFilter(django_filters.FilterSet):

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Order
        fields = ["number", "id_user", "id_master",]
    
class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
class MasterViewSet(viewsets.ModelViewSet):

    queryset = Master.objects.all()
    serializer_class = MasterSerializer

class SpecialityViewSet(viewsets.ModelViewSet):

    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

class OrderViewSet(viewsets.ModelViewSet):

    filter_backends = [SearchFilter, DjangoFilterBackend] 
    search_fields = ["number", "price"]
    filterset_class = OrderFilter
    queryset = Order.objects.all()
    serializer_class = OrderSerializer    