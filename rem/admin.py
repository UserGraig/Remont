from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from .models import Client, Master, Order,Speciality

class MasterResource(resources.ModelResource):

    class Meta:

        model = Master
        fields = (
            "username",
            "description",
            "speciality",
            "rating",
        )
    def dehydrate_rating(self, obj):
        return f"{obj.rating:.2f}"
    def dehydrate_description(self, instance):
        return instance.description or "Описание отсутствует"
    
class ClientResource(resources.ModelResource):

    class Meta:

        model = Client
        fields = (
            "username",
            "email",
            "created_at",
        )

    def dehydrate_email(self, instance):
        return instance.email or "email не указан"


admin.site.register(Speciality)
admin.site.register(Order)

@admin.register(Client)
class ClientAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    resource_class = ClientResource
    list_display = ["username", "email", "created_at"]
    list_editable = ["email"]
    search_fields = ("username", "email")
    date_hierarchy = "created_at"

@admin.register(Master)
class MasterAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = MasterResource
    list_display = ["username", "speciality", "rating"]
    list_filter = ["speciality"]






