# Generated by Django 4.0 on 2021-12-28 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_app", "0011_alter_documentrequest_status_request"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentrequest",
            name="status_request",
            field=models.CharField(
                choices=[
                    ("INITIATED_STATUS", "initiated"),
                    ("RECEIVED_STATUS", "received"),
                ],
                max_length=50,
            ),
        ),
    ]
