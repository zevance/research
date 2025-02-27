# Generated by Django 4.1.5 on 2023-11-29 06:26

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
            name='Call',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Grant', 'Grant'), ('Project', 'Project'), ('Consultancy', 'Consultancy')], max_length=100)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=50)),
                ('document', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
