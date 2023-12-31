# Generated by Django 4.2.6 on 2023-12-07 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ent_infoConnect', '0014_alter_agenda_options_alter_annonce_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='matricule',
            field=models.ForeignKey(blank=True, db_column='matricule', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.etudiant'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='matricule_en',
            field=models.ForeignKey(blank=True, db_column='matricule_en', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.enseignant'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='matricule',
            field=models.ForeignKey(blank=True, db_column='matricule', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.etudiant'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='matricule_en',
            field=models.ForeignKey(blank=True, db_column='matricule_en', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.enseignant'),
        ),
        migrations.AddField(
            model_name='document',
            name='matricule',
            field=models.ForeignKey(blank=True, db_column='matricule', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.etudiant'),
        ),
        migrations.AddField(
            model_name='document',
            name='matricule_en',
            field=models.ForeignKey(blank=True, db_column='matricule_en', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.enseignant'),
        ),
        migrations.AddField(
            model_name='note',
            name='code_ue',
            field=models.ForeignKey(blank=True, db_column='code_ue', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.ue'),
        ),
        migrations.AddField(
            model_name='note',
            name='matricule',
            field=models.ForeignKey(blank=True, db_column='matricule', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.etudiant'),
        ),
        migrations.AddField(
            model_name='note',
            name='matricule_en',
            field=models.ForeignKey(blank=True, db_column='matricule_en', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.enseignant'),
        ),
        migrations.AddField(
            model_name='profilens',
            name='matricule_en',
            field=models.ForeignKey(blank=True, db_column='matricule_en', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.enseignant'),
        ),
        migrations.AddField(
            model_name='profiletu',
            name='matricule',
            field=models.ForeignKey(blank=True, db_column='matricule', null=True, on_delete=django.db.models.deletion.CASCADE, to='ent_infoConnect.etudiant'),
        ),
    ]
