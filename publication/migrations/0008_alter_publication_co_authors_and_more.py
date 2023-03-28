# Generated by Django 4.1.5 on 2023-03-27 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0007_remove_publicationauthor_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='co_authors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='number_of_pages',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
