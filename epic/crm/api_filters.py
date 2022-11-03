from django_filters import rest_framework as filters

from crm.models import Customer, Contract


class CustomerFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr="iexact")
    last_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Customer
        fields = ["last_name", "email"]


class ContractFilter(filters.FilterSet):
    customer__email = filters.CharFilter(lookup_expr="iexact")

    customer__last_name = filters.CharFilter(lookup_expr="icontains")

    amount = filters.NumberFilter()
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")

    date_created = filters.DateFilter(field_name="date_created", lookup_expr="d")
    date_created__gte = filters.DateFilter(
        field_name="date_created", lookup_expr="date_created__gte"
    )
    date_created__lte = filters.DateFilter(
        field_name="date_created", lookup_expr="date_created__lte"
    )

    class Meta:
        model = Contract
        fields = ["customer__last_name", "customer__email", "date_created", "amount"]


class EventFilter(filters.FilterSet):
    customer__email = filters.CharFilter(lookup_expr="iexact")

    customer__last_name = filters.CharFilter(lookup_expr="icontains")

    event_date = filters.DateFilter(field_name="event_date", lookup_expr="d")
    event_date__gte = filters.DateFilter(
        field_name="event_date", lookup_expr="event_date__gte"
    )
    event_date__lte = filters.DateFilter(
        field_name="event_date", lookup_expr="event_date__lte"
    )

    class Meta:
        model = Contract
        fields = ["customer__last_name", "customer__email", "event_date"]
