# Generated by Django 4.1.5 on 2023-02-06 08:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('contact_address', models.TextField()),
                ('contact_number', models.IntegerField()),
                ('country', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPartners',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.partner')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMembers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.member')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.project')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.role')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDocuments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.FileField(blank=True, upload_to='project_documents/%Y/%m/%d/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.project')),
            ],
        ),
        migrations.CreateModel(
            name='DonorProjects',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.donor')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.project')),
            ],
        ),
    ]
