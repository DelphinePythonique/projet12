from django.db.models import Q
from importlib._common import _

from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Status, Customer, Contract, Event

User = get_user_model()


class CustomerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        sales_group = Group.objects.filter(name="sales_team")[0]
        if db_field.name == "sales_contact":
            kwargs["queryset"] = User.objects.filter(groups=sales_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(sales_contact=request.user)
            | Q(contract_to__sales_contact=request.user)
            | Q(organise__support_contact=request.user)
        )


admin.site.register(Customer, CustomerAdmin)

admin.site.register(Status)


class ContractAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        sales_group = Group.objects.filter(name="sales_team")[0]
        if db_field.name == "sales_contact":
            kwargs["queryset"] = User.objects.filter(groups=sales_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(sales_contact=request.user)
            | Q(customer__sales_contact=request.user)
          
        )


admin.site.register(Contract, ContractAdmin)


class EventAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        support_group = Group.objects.filter(name="support_team")[0]
        if db_field.name == "support_contact":
            kwargs["queryset"] = User.objects.filter(groups=support_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(support_contact=request.user)
            | Q(customer__sales_contact=request.user)
            | Q(customer__contract_to__sales_contact=request.user)
        )


admin.site.register(Event, EventAdmin)
