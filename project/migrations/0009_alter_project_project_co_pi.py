# Generated by Django 4.1.5 on 2023-11-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_alter_project_umbrella_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_co_pi',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
