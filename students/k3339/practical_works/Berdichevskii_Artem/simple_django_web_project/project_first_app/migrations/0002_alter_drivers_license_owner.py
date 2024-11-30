# Generated by Django 5.1.2 on 2024-10-09 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_first_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="drivers_license",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="project_first_app.owner",
            ),
        ),
    ]
