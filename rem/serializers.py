from rest_framework import serializers
from .models import Client, Master, Order, Speciality, Service, Review

class ClientSerializer(serializers.ModelSerializer):

    class Meta:

        model = Client
        fields = "__all__"
    def validate_email(self, value):
        if not (value.endswith("@gmail.com") or value.endswith("@mail.ru")):
            raise serializers.ValidationError("Email-адрес должен заканчиваться на @gmail.com или @mail.ru.")
        return value


class MasterSerializer(serializers.ModelSerializer):

    class Meta:

        model = Master
        fields = "__all__"        
    def validate_rating(self, value):

        if (value < 1) or (value > 5):
            raise serializers.ValidationError("Рейтинг может быть от 1 до 5.")
        return value
        


class OrderSerializer(serializers.ModelSerializer):
    class Meta:

        model = Order
        fields = "__all__"
    def validate_price(self, value):

        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value


class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:

        model = Speciality
        fields = "__all__"                

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Service
        fields = "__all__"   

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:

        model = Review
        fields = "__all__"   

