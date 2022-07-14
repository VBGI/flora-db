# Generated by Django 2.2.5 on 2022-07-14 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flora', '0007_auto_20220712_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='area',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='area',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='location',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='occurrences', to='flora.Location'),
        ),
        migrations.AlterField(
            model_name='location',
            name='abbr',
            field=models.CharField(default='', max_length=10),
        ),
    ]
