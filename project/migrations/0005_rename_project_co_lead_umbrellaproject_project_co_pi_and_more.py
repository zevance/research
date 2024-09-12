# Generated by Django 4.1.5 on 2023-07-08 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_umbrellaproject_project_umbrella_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='umbrellaproject',
            old_name='project_co_lead',
            new_name='project_co_pi',
        ),
        migrations.RenameField(
            model_name='umbrellaproject',
            old_name='project_lead',
            new_name='project_pi',
        ),
        migrations.AlterField(
            model_name='project',
            name='umbrella_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.umbrellaproject'),
        ),
    ]
