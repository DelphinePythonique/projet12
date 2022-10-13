from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

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

    serializer_class = CustomerListSerializer
    detail_serializer_class = CustomerDetailSerializer


    def get_queryset(self):

        return Customer.objects.all()