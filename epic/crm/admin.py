from django.contrib import admin

# Register your models here.
from .models import Status, Customer, Contract, Event

admin.site.register(Status)
admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(Event)
