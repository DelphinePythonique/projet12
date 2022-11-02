from django.conf import settings
from django.db import models

# Create your models here.
STATUS_CONTRACT = [
    ("S", "Sign"),
    ("QS", "Quote sent"),
    ("P", "In progress"),
]


def get_help_text(calling_class, choices):
    text = [f"This field is used to categorize the {calling_class}. Use"]
    text.extend([f"{choice[0]}=>{choice[1]}" for choice in choices])
    return ", ".join(text)


class Customer(models.Model):
    first_name = models.CharField(max_length=25, help_text="customer's firstname")
    last_name = models.CharField(max_length=25, help_text="customer's lastname")
    email = models.CharField(
        max_length=100, null=True, blank=True, help_text="customer's email"
    )
    phone = models.CharField(
        max_length=20, null=True, blank=True, help_text="customer's phone"
    )
    mobile = models.EmailField(
        max_length=20, null=True, blank=True, help_text="customer's mobile"
    )
    company_name = models.CharField(
        max_length=200, null=True, blank=True, help_text="customer's company name"
    )
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="customer's sale contact",
    )
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="customer's creation date"
    )
    date_updated = models.DateTimeField(
        auto_now=True, help_text="customer's update date"
    )

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
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="contract's sale",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="contract_to",
        help_text="contract's customer",
    )
    status = models.CharField(
        max_length=3,
        default="P",
        choices=STATUS_CONTRACT,
        help_text=get_help_text("project", STATUS_CONTRACT),
    )
    amount = models.FloatField(default=0, help_text="contract's amount")
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="contract's creation date"
    )
    date_updated = models.DateTimeField(
        auto_now=True, help_text="contract's update date"
    )
    payment_due = models.DateTimeField(
        null=True, blank=True, help_text="contract's paiement due date"
    )

    def __str__(self):
        return f"{self.customer} {self.date_created}"


class Event(models.Model):
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="event's support",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="organise",
        help_text="event's customer",
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="event's status",
    )
    attendees = models.PositiveIntegerField(
        default=0, help_text="event's number of attendees"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="event's creation date"
    )
    date_updated = models.DateTimeField(auto_now=True, help_text="event's update date")
    event_date = models.DateTimeField(null=True, blank=True, help_text="event's date")
    notes = models.TextField(null=True, blank=True, help_text="event's note")

    def __str__(self):
        return f"{self.customer} - {self.event_date}"
