# Generated by Django 4.1.5 on 2024-02-06 08:39

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
            name='Grant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount_of_funding', models.FloatField()),
                ('title', models.CharField(max_length=255)),
                ('abstract', models.TextField()),
                ('introduction', models.TextField()),
                ('justification', models.TextField()),
                ('objectives', models.TextField()),
                ('methodology', models.TextField()),
                ('research_dessemination_strategy', models.TextField()),
                ('ethical_considerations', models.TextField()),
                ('budget', models.FileField(upload_to='grants/')),
                ('resume', models.FileField(upload_to='grants/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
