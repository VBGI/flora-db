# Generated by Django 2.2.5 on 2022-07-12 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flora', '0005_auto_20191007_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='', max_length=50)),
                ('info', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
    ]
