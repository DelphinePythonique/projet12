from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.viewsets import GenericViewSet

from .permissions import permissions_filter_on_customer
from .serializers import CustomerListSerializer, CustomerDetailSerializer

from .models import Customer


class CustomerViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    list:
    Return the list of customers

    create:
    add a customer.

    retrieve:
    Return a customer .


    destroy:
    delete a customer

    """

    schema = AutoSchema(
        tags=["customer", "crm"],
        component_name="Customer",
        operation_id_base="Customer",
    )
    serializer_class = CustomerListSerializer
    detail_serializer_class = CustomerDetailSerializer

    def get_queryset(self):
        customer_queryset_with_permissions = permissions_filter_on_customer(
            Customer.objects.all(), self.request.user
        )
        return customer_queryset_with_permissions
