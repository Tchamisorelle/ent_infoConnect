# Generated by Django 4.2.6 on 2023-11-13 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("ent_infoConnect", "0007_etudiant_password"),
    ]

    operations = [
        migrations.RemoveField(model_name="resetlink", name="user_type",),
        migrations.AddField(
            model_name="enseignant",
            name="password",
            field=models.CharField(default=1, max_length=128, verbose_name="password"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resetlink",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resetlink",
            name="object_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
