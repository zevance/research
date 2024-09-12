# Generated by Django 4.1.5 on 2023-02-08 12:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorRank',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Innovation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('patent', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('abstract', models.TextField()),
                ('publication_link', models.CharField(max_length=255, unique=True)),
                ('year_of_publication', models.IntegerField()),
                ('place_of_publication', models.CharField(max_length=255)),
                ('isbn', models.CharField(max_length=255, unique=True)),
                ('publisher', models.CharField(max_length=255)),
                ('tags', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.collection')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.license')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResearcherPublication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('author_rank', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.authorrank')),
                ('author_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.authortype')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.publication')),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.researcher')),
            ],
        ),
        migrations.CreateModel(
            name='ResearcherInnovation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('innovation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.innovation')),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.researcher')),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.publicationtype'),
        ),
        migrations.CreateModel(
            name='InnovationMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('media', models.FileField(blank=True, upload_to='innovation_media/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('innovation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.innovation')),
            ],
        ),
    ]
