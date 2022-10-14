from django.conf import settings
from django.db import models

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.EmailField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def contracts(self):
        return self.contract_to.all()

    @property
    def events(self):
        return self.organise.all()

    @property
    def contributors(self):
        sales_contacts = [contract.sales_contact for contract in self.contracts]
        support_contacts = [event.sales_contact for event in self.events]
        return list(set(support_contacts) + set(sales_contacts))


class Status(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract_to",
    )
    status = models.BooleanField(null=True, blank=True)
    amount = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    payment_due = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer} {self.date_created}"


class Event(models.Model):
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organise",
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    attendees = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer} - {self.event_date}"
