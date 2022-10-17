from django.contrib.auth.models import Group
from rest_framework import serializers
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

    def validate_sales_contact(self, user):
        group_ = Group.objects.get(name="sales_team")

        if group_ not in user.groups.all():
            message = f"User mut be in the {group_.name}."
            raise serializers.ValidationError(message)
        return user


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
