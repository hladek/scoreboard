# Generated by Django 4.1.1 on 2023-01-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contest", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="duration",
            field=models.FloatField(null=True),
        ),
    ]
