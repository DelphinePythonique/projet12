from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Customer, Contract, Event


class CustomerListSerializer(ModelSerializer):
    sales_contact = serializers.SlugRelatedField(
        queryset=get_user_model().objects.filter(groups__name="sales_team"),
        slug_field="username",
    )

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "sales_contact",
            "email",
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


class ContractListSerializer(ModelSerializer):
    sales_contact = serializers.SlugRelatedField(
        queryset=get_user_model().objects.filter(groups__name="sales_team"),
        slug_field="username",
    )

    customer = serializers.ReadOnlyField(source="customer.last_name")
    status = serializers.ReadOnlyField(source="status.name")

    class Meta:
        model = Contract
        fields = [
            "sales_contact",
            "customer",
            "status",
            "amount",
            "payment_due",
        ]

    def validate_sales_contact(self, user):
        group_ = Group.objects.get(name="sales_team")

        if group_ not in user.groups.all():
            message = f"User mut be in the {group_.name}."
            raise serializers.ValidationError(message)
        return user


class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "sales_contact",
            "customer",
            "status",
            "amount",
            "payment_due",
        ]


class EventListSerializer(ModelSerializer):
    support_contact = serializers.SlugRelatedField(
        queryset=get_user_model().objects.filter(groups__name="support_team"),
        slug_field="username",
    )
    customer__last_name = serializers.ReadOnlyField(source="customer.last_name")
    customer__email = serializers.ReadOnlyField(source="customer.email")
    status = serializers.ReadOnlyField(source="status.name")

    class Meta:
        model = Event
        fields = [
            "support_contact",
            "customer__last_name",
            "customer__email",
            "status",
            "attendees",
            "event_date",
        ]

    def validate_support_contact(self, user):
        group_ = Group.objects.get(name="support_team")

        if group_ not in user.groups.all():
            message = f"User must be in the {group_.name}."
            raise serializers.ValidationError(message)
        return user


class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "support_contact",
            "customer",
            "status",
            "attendees",
            "event_date",
            "notes",
        ]
