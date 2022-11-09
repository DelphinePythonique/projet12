# Generated by Django 4.1.1 on 2022-11-02 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0007_alter_contract_amount_alter_contract_customer_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="customer",
            field=models.ForeignKey(
                help_text="contract's customer",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contract_to",
                to="crm.customer",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="customer",
            field=models.ForeignKey(
                help_text="event's customer",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organise",
                to="crm.customer",
            ),
        ),
    ]
