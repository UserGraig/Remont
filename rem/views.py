"""
Этот модуль содержит представления приложения, включая 
API для моделей Client, Order, Speciality, Master, Service 
и Review. Каждый ViewSet предоставляет операции CRUD, а также 
настраиваемые действия.
"""

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Client, Order, Speciality, Master, Service, Review
from .serializers import (
    ClientSerializer,
    SpecialitySerializer,
    OrderSerializer,
    MasterSerializer,
    ServiceSerializer,
    ReviewSerializer,
)

from django.core.cache import cache
from django.shortcuts import get_list_or_404
from .models import Task # Импортируйте вашу модель Task


class OrderPriceSerializer(serializers.ModelSerializer):
    """ 
    Сериализатор для модели Order, 
    используемый для обновления цены заказа. 
    """

    class Meta:
        model = Order
        fields = ["price"]

    def validate_price(self, value):
        """
        Проверяет, что цена не ниже 0.
        """
        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value



class OrderFilter(django_filters.FilterSet):
    """
    Фильтр для модели Order. 
    Позволяет фильтровать заказы по цене и другим атрибутам.
    """
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Order
        fields = ["number", "id_user", "id_master"]



class ClientViewSet(viewsets.ModelViewSet):
    """
    API для управления клиентами. 
    Предоставляет операции CRUD для модели Client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer



class MasterViewSet(viewsets.ModelViewSet):
    """
    API для управления мастерами. 
    Предоставляет операции CRUD и статистику по мастерам.
    """
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

    @action(methods=["GET"], detail=False)
    def statistics(self, request):
        """
        Возвращает статистику по мастерам 
        и количество каждой специальности.
        """
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

    @action(methods=["GET"], detail=False)
    def pro(self, request):
        """
        Возвращает мастеров с определенными условиями 
        в зависимости от их специальности и рейтинга.
        """
        professionals = Master.objects.filter(
            ((Q(speciality__name='Электрик') | Q(speciality__name='Маляр')) & Q(rating__gte=4)) &
            ~Q(order__id_user__email__endswith="gmail.com")
        )
        professionals2 = Master.objects.filter(
            ((Q(speciality__name='Сантехник') | Q(speciality__name='Плотник')) & Q(rating__lte=3)) &
            ~Q(order__id_user__email__endswith="mail.ru")
        )

        serializer1 = MasterSerializer(professionals, many=True)
        serializer2 = MasterSerializer(professionals2, many=True)

        return Response(
            {
                "Мастеры (электрики или маляры) с рейтингом выше или равно 4. "
                "Почта клиентов не оканчивается на 'gmail.com'": serializer1.data,
                "Мастеры (сантехники или плотники) с рейтингом ниже или равно 3. "
                "Почта клиентов не оканчивается на 'mail.ru'": serializer2.data,
            }
        )



class SpecialityViewSet(viewsets.ModelViewSet):
    """
    API для управления специальностями. 
    Предоставляет операции CRUD для модели Speciality.
    """
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer



class OrderViewSet(viewsets.ModelViewSet):
    """
    API для управления заказами. 
    Предоставляет операции CRUD и настраиваемые действия для заказов.
    """
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["number", "price"]
    filterset_class = OrderFilter
    queryset = Order.objects.all()
    serializer_class = OrderSerializer    

    @action(methods=["POST"], detail=True)
    def change_price(self, request, pk=None):
        """
        Изменяет цену заказа по его ID.
        """
        order = self.get_object()
        serializer = OrderPriceSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Цена заказа изменена."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор для 
        конкретных действий, таких как "change_price".
        """
        if self.action == "change_price":
            return OrderPriceSerializer
        return super().get_serializer_class()



class ServiceViewSet(viewsets.ModelViewSet):
    """
    API для управления услугами. 
    Предоставляет операции CRUD для модели Service.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    """
    API для управления отзывами. 
    Предоставляет операции CRUD для модели Review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



from django.core.mail import send_mail

def send_welcome_email(client_email):
    subject = 'Добро пожаловать!'
    message = 'Спасибо за регистрацию в нашем сервисе.'
    from_email = 'noreply@example.com'
    
    send_mail(subject, message, from_email, [client_email])


def get_user_tasks(user):
    cache_key = f"user_tasks_{user.id}"
    tasks = cache.get(cache_key)
    
    if tasks is None:
        tasks = get_list_or_404(Task, owner=user)
        cache.set(cache_key, tasks, timeout=60 * 15)  # Кэш на 15 минут
        
    return tasks
