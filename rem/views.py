import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from .models import Client, Order, Speciality, Master
from .serializers import ClientSerializer, SpecialitySerializer, OrderSerializer, MasterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count


# Create your views here.
class OrderPriceSerializer(serializers.ModelSerializer):

    class Meta:
     
        model = Order
        fields = ["price"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value


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
    @action(methods=["GET"], detail=False)
    def statistics(self, request):
        all_count = self.get_queryset().count()
        speciality_count = (
            self.get_queryset().values("speciality__name").annotate(count=Count("id"))
        )

        return Response(
            {
                "Всего специальностей": all_count,
                "Статистика по специальностям": speciality_count,
            }
        )



class SpecialityViewSet(viewsets.ModelViewSet):

    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
   


class OrderViewSet(viewsets.ModelViewSet):

    filter_backends = [SearchFilter, DjangoFilterBackend] 
    search_fields = ["number", "price"]
    filterset_class = OrderFilter
    queryset = Order.objects.all()
    serializer_class = OrderSerializer    
    @action(methods=["POST"], detail=True)
    def change_price(self, request, pk=None):
        order = self.get_object()
        serializer = OrderPriceSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Цена заказа изменена."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "change_price":
            return OrderPriceSerializer
        return super().get_serializer_class()
