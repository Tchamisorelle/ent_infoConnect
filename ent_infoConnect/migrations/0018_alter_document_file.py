# Generated by Django 4.2.6 on 2023-12-24 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ent_infoConnect", "0017_remove_document_matricule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="documents/"),
        ),
    ]
