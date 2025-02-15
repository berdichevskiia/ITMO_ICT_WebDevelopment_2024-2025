# Generated by Django 5.1.2 on 2024-10-25 08:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project_first_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": [
                    ("add_logentry", "Can add log entry"),
                    ("change_logentry", "Can change log entry"),
                    ("delete_logentry", "Can delete log entry"),
                    ("view_logentry", "Can view log entry"),
                    ("add_group", "Can add group"),
                    ("change_group", "Can change group"),
                    ("delete_group", "Can delete group"),
                    ("view_group", "Can view group"),
                    ("add_permission", "Can add permission"),
                    ("change_permission", "Can change permission"),
                    ("delete_permission", "Can delete permission"),
                    ("view_permission", "Can view permission"),
                    ("add_contenttype", "Can add content type"),
                    ("change_contenttype", "Can change content type"),
                    ("delete_contenttype", "Can delete content type"),
                    ("view_contenttype", "Can view content type"),
                    ("add_conference", "Can add conference"),
                    ("change_conference", "Can change conference"),
                    ("delete_conference", "Can delete conference"),
                    ("view_conference", "Can view conference"),
                    ("add_participant", "Can add participant"),
                    ("change_participant", "Can change participant"),
                    ("delete_participant", "Can delete participant"),
                    ("view_participant", "Can view participant"),
                    ("add_presentationresult", "Can add presentation result"),
                    ("change_presentationresult", "Can change presentation result"),
                    ("delete_presentationresult", "Can delete presentation result"),
                    ("view_presentationresult", "Can view presentation result"),
                    ("add_review", "Can add review"),
                    ("change_review", "Can change review"),
                    ("delete_review", "Can delete review"),
                    ("view_review", "Can view review"),
                    ("add_session", "Can add session"),
                    ("change_session", "Can change session"),
                    ("delete_session", "Can delete session"),
                    ("view_session", "Can view session"),
                ]
            },
        ),
    ]
