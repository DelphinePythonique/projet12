from django.conf import settings
from django.db import models

# Create your models here.
STATUS_CONTRACT = [
    ("S", "Sign"),
    ("QS", "Quote sent"),
    ("P", "In progress"),
]


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
    status = models.CharField(max_length=3, default="P", choices=STATUS_CONTRACT)
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
