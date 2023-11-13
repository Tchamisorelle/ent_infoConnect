# Generated by Django 4.2.6 on 2023-11-13 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ent_infoConnect", "0010_enseignant_password_etudiant_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="resetlink",
            name="user_type",
            field=models.CharField(
                choices=[("ETUDIANT", "Etudiant"), ("ENSEIGNANT", "Enseignant")],
                default=1,
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="resetlink",
            name="object_id",
            field=models.CharField(max_length=255),
        ),
    ]
