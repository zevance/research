# Generated by Django 4.1.5 on 2023-07-08 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_rename_project_co_lead_umbrellaproject_project_co_pi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='umbrella_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.umbrellaproject'),
        ),
    ]
