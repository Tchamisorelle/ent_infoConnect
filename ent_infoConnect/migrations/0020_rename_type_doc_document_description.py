# Generated by Django 4.2.6 on 2023-12-27 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ent_infoConnect", "0019_alter_document_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="document", old_name="type_doc", new_name="description",
        ),
    ]