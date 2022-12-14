from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Status, Customer, Contract, Event
from .permissions import (
    permissions_filter_on_customer,
    is_change_authorized,
    permissions_filter_on_contract,
    permissions_filter_on_event,
)
from .admin_filters import TextFilter, NumericRangeFilter, DateRangeFilter

User = get_user_model()


class CustomerAdmin(admin.ModelAdmin):

    list_display = ("first_name", "last_name", "email", "sales_contact")
    list_filter = (("last_name", TextFilter), ("email", TextFilter))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        sales_group = Group.objects.filter(name="sales_team")[0]
        if db_field.name == "sales_contact":
            kwargs["queryset"] = User.objects.filter(groups=sales_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return permissions_filter_on_customer(qs, request)

    def has_change_permission(self, request, obj=None):
        allowed = super().has_change_permission(request, obj)

        if obj is None:
            return allowed
        return is_change_authorized(request, obj)


admin.site.register(Customer, CustomerAdmin)

admin.site.register(Status)


class ContractAdmin(admin.ModelAdmin):
    list_display = ("customer", "sales_contact", "status", "amount", "payment_due")
    list_filter = (
        ("customer__last_name", TextFilter),
        ("customer__email", TextFilter),
        ("date_created", DateRangeFilter),
        ("amount", NumericRangeFilter),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        sales_group = Group.objects.filter(name="sales_team")[0]
        if db_field.name == "sales_contact":
            kwargs["queryset"] = User.objects.filter(groups=sales_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return permissions_filter_on_contract(qs, request)

    def has_change_permission(self, request, obj=None):
        allowed = super().has_change_permission(request, obj)

        if obj is None:
            return allowed
        return is_change_authorized(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == "S":
            event = Event(customer=obj.customer)
            event.save()


admin.site.register(Contract, ContractAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("customer", "support_contact", "status", "attendees", "event_date")
    list_filter = (
        ("customer__last_name", TextFilter),
        ("customer__email", TextFilter),
        ("event_date", DateRangeFilter),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        support_group = Group.objects.filter(name="support_team")[0]
        if db_field.name == "support_contact":
            kwargs["queryset"] = User.objects.filter(groups=support_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return permissions_filter_on_event(qs, request)

    def has_change_permission(self, request, obj=None):
        allowed = super().has_change_permission(request, obj)

        if obj is None:
            return allowed
        return is_change_authorized(request, obj)


admin.site.register(Event, EventAdmin)
