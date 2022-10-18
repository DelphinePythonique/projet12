
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.viewsets import GenericViewSet

from .permissions import (
    permissions_filter_on_customer,
    IsOwner,
    permissions_filter_on_contract, permissions_filter_on_event,
)
from .serializers import (
    CustomerListSerializer,
    CustomerDetailSerializer,
    ContractDetailSerializer,
    ContractListSerializer,
    EventListSerializer,
    EventDetailSerializer,
)

from .models import Customer, Contract, Event


class CustomerViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
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

    update:
    update a customer

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']
    permission_classes = [IsAuthenticated & (DjangoModelPermissions | IsOwner)]

    def get_queryset(self):
        customer_queryset_with_permissions = permissions_filter_on_customer(
            Customer.objects.all(), self.request
        )
        return customer_queryset_with_permissions


class ContractViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    list:
    Return the list of contracts

    create:
    add a contract.

    retrieve:
    Return a contract .

    update:
    update a contract

    destroy:
    delete a contract

    """

    schema = AutoSchema(
        tags=["contract", "crm"],
        component_name="contract",
        operation_id_base="Contract",
    )
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated & (DjangoModelPermissions | IsOwner)]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["customer__last_name", "customer__email", "date_created", "amount"]

    def get_queryset(self):
        contract_queryset_with_permissions = permissions_filter_on_contract(
            Contract.objects.all(), self.request
        )
        return contract_queryset_with_permissions


class EventViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    list:
    Return the list of events

    create:
    add an event.

    retrieve:
    Return an event.

    update:
    update an event.

    destroy:
    delete an event.

    """

    schema = AutoSchema(
        tags=["event", "crm"],
        component_name="event",
        operation_id_base="event",
    )
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated & (DjangoModelPermissions | IsOwner)]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["customer__last_name", "customer__email", "event_date"]

    def get_queryset(self):
        event_queryset_with_permissions = permissions_filter_on_event(
            Event.objects.all(), self.request
        )
        return event_queryset_with_permissions
