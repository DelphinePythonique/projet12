# Generated by Django 4.1.1 on 2022-10-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0005_alter_contract_customer_alter_contract_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="status",
            field=models.CharField(
                choices=[("S", "Sign"), ("QS", "Quote sent"), ("P", "In progress")],
                default="P",
                max_length=3,
            ),
        ),
    ]