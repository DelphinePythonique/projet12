from rest_framework.serializers import ModelSerializer

from .models import Customer


class CustomerListSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "sales_contact",
        ]


class CustomerDetailSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "company_name",
            "sales_contact",
        ]