# Generated by Django 4.2.6 on 2023-12-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ent_infoConnect", "0015_agenda_matricule_agenda_matricule_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
