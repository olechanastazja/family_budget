# Generated by Django 4.1.1 on 2022-09-05 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget_core", "0004_alter_budget_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetitem",
            name="item_type",
            field=models.CharField(
                choices=[("EXPENSE", "EXPENSE"), ("INCOME", "INCOME")],
                default="INCOME",
                max_length=32,
            ),
        ),
    ]
