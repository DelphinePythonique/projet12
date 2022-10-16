from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework.permissions import BasePermission

from .models import Customer, Contract, Event


def permissions_filter_on_customer(customer_queryset, request):
    group_ = Group.objects.filter(name="management_team")[0]
    if group_ in request.user.groups.all():
        return customer_queryset
    if request.user.is_superuser:
        return customer_queryset

    return customer_queryset.filter(
        Q(sales_contact=request.user)
        | Q(contract_to__sales_contact=request.user)
        | Q(organise__support_contact=request.user)
    )


def is_change_authorized(request, obj):
    group_ = Group.objects.filter(name="management_team")[0]
    if group_ in request.user.groups.all():
        return True
    if request.user.is_superuser:
        return True
    if is_owner(request, obj):
        return True


def is_owner(request, obj):

    if isinstance(obj, Customer):
        return obj.sales_contact == request.user
    if isinstance(obj, Contract):
        return obj.sales_contact == request.user
    if isinstance(obj, Event):
        return obj.support_contact == request.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in SAFE_METHODS:
        #    return True
        return is_owner(request, obj)
