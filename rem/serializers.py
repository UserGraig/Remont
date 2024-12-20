"""
Этот модуль содержит сериализаторы для моделей проекта.
Они используются для преобразования моделей в JSON-репрезентации и для валидации входящих данных.
"""

from rest_framework import serializers
from .models import Client, Master, Order, Speciality, Service, Review

class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Клиент."""

    class Meta:
        model = Client  # Модель для сериализации
        fields = "__all__"  # Включить все поля модели

    def validate_email(self, value):
        """Проверка корректности email клиента."""
        if not (value.endswith("@gmail.com") or value.endswith("@mail.ru")):
            raise serializers.ValidationError(
                "Email-адрес должен заканчиваться на @gmail.com или @mail.ru."
            )
        return value  # Возвращает корректное значение


class MasterSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Мастер."""

    class Meta:
        model = Master  # Модель для сериализации
        fields = "__all__"  # Включить все поля модели

    def validate_rating(self, value):
        """Проверка рейтинга мастера."""
        if (value < 1) or (value > 5):
            raise serializers.ValidationError("Рейтинг может быть от 1 до 5.")
        return value  # Возвращает корректное значение


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Заказ."""

    class Meta:
        model = Order  # Модель для сериализации
        fields = "__all__"  # Включить все поля модели

    def validate_price(self, value):
        """Проверка цены заказа."""
        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value  # Возвращает корректное значение


class SpecialitySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Специальность."""

    class Meta:
        model = Speciality  # Модель для сериализации
        fields = "__all__"  # Включить все поля модели


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Услуга."""

    class Meta:
        model = Service  # Модель для сериализации
        fields = "__all__"  # Включить все поля модели


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзыв."""

    class Meta:
        model = Review  # Модель для сериализации
        fields = "__all__"  # Включить все поля модели
